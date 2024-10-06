import json
import os
from datetime import UTC, date, datetime
from pathlib import Path
from types import NoneType, UnionType
from typing import Any, Self, TypeAlias, get_args, get_origin, get_type_hints

from dotenv import dotenv_values

from .exceptions import SettingsValidationException

__all__ = ["SettingsMetaclass", "SettingsConfig", "SettingsBase"]

_AllowedSettingsTypeAlias: TypeAlias = str | int | bool | float | Path | datetime | date | list
_AllowedSettingsListTypeAlias: TypeAlias = str | int | float | Path | datetime | date
_ALLOWED_SETTINGS_TYPES = get_args(_AllowedSettingsTypeAlias)
_ALLOWED_SETTINGS_LIST_TYPES = get_args(_AllowedSettingsListTypeAlias)
_ALLOWED_SETTINGS_TYPES_REPR = (
    f'({", ".join([tp.__name__ if type(tp) is type else str(tp) for tp in _ALLOWED_SETTINGS_TYPES])})'
)
_ALLOWED_SETTINGS_LIST_TYPES_REPR = (
    f'({", ".join([("list[" + tp.__name__ + "]") for tp in _ALLOWED_SETTINGS_LIST_TYPES])})'
)


def fromisoformat_safe(value: str) -> datetime | None:
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except:
        return None


class UnparsedValue: ...


class SettingsConfig:
    __prefix: str
    __secrets_dir: str
    __env_file: str

    def __init__(
        self,
        prefix: str = "",
        secrets_dir: str = "/run/secrets",
        env_file: str = ".h8appsettings",
    ) -> None:
        self.__prefix = prefix
        self.__secrets_dir = secrets_dir
        self.__env_file = env_file

    @property
    def prefix(self):
        return self.__prefix

    @property
    def secrets_dir(self):
        return self.__secrets_dir

    @property
    def env_file(self):
        return self.__env_file

    def __get__(self, obj, objtype=None) -> Self:
        return self

    def __set__(self, obj, value: Any):
        raise RuntimeError("SettingsConfig cannot be change once defined.")


class SettingsMetaclass(type):

    def __init__(cls, objname, bases, clsdict) -> None:
        if bases and len(bases) > 1:
            raise ValueError(f"{objname} class cannot inherit from multiple classes")

        if bases and bases[0] is SettingsBase:
            settings_config: SettingsConfig | None = getattr(cls, "settings_config")
            if settings_config is None:
                cls.settings_config = SettingsConfig()
                settings_config = cls.settings_config

            env: dict[str, Any] = {
                **cls.__load_secrets_dir(settings_config),
                **cls.__load_env(settings_config),
            }

            for (
                attr_name,
                type_hint,
            ) in get_type_hints(cls).items():
                if attr_name == "settings_config":
                    continue

                exists_in_env = attr_name.lower() in env
                has_default = hasattr(cls, attr_name)

                input_value = env.get(attr_name.lower())
                if not exists_in_env and has_default:
                    input_value = getattr(cls, attr_name)

                origin = get_origin(type_hint)
                type_args = get_args(type_hint)
                attr_type = type_hint
                type_hint_repr = type_hint if type(type_hint) is not type else type_hint.__name__

                if (
                    origin is UnionType
                    and (
                        len(type_args) != 2
                        or NoneType not in type_args
                        or not any(
                            ta in _ALLOWED_SETTINGS_TYPES or get_origin(ta) is list for ta in type_args
                        )
                    )
                    or origin is None
                    and type_hint not in _ALLOWED_SETTINGS_TYPES
                ):
                    raise SettingsValidationException(
                        f"Invalid type annotation at '{objname}' class. Attribute '{attr_name}' cannot be declared as '{type_hint_repr}'. "
                        f"\n\t\t -> Only one of allowed types {_ALLOWED_SETTINGS_TYPES_REPR} is permitted. "
                        "\n\t\t -> It can be combinable with None to annotate nullable attributes."
                    )

                nullable = False
                if origin is UnionType:
                    # Nullable attribute here.
                    attr_type = [tp for tp in type_args if tp is not NoneType][0]
                    nullable = True

                is_list_type = get_origin(attr_type) is list or attr_type is list

                if is_list_type:
                    cls.__validate_list_annotation(objname, attr_name, attr_type, type_hint)

                try:
                    if is_list_type:
                        attr_value = cls.__cast_list(
                            objname=objname,
                            attr_name=attr_name,
                            value=input_value,
                            type_hint_repr=type_hint_repr,
                            _type=attr_type,
                        )

                    else:
                        attr_value = cls.__cast(
                            objname=objname,
                            attr_name=attr_name,
                            type_hint_repr=type_hint_repr,
                            value=input_value,
                            _type=attr_type,
                            nullable=nullable,
                        )

                    setattr(cls, attr_name, attr_value)

                except TypeError as e:
                    raise TypeError(
                        f"Invalid value type for attribute '{attr_name}' of type '{type_hint_repr}' declared in "
                        f"'{objname}' object.\nInput value: {input_value or None}"
                    ) from e

                except ValueError as e:
                    raise ValueError(
                        f"Invalid value for attribute '{attr_name}' of type '{type_hint_repr}' declared in "
                        f"'{objname}' object.\nInput value: {input_value or None}"
                    ) from e

                except RuntimeError as e:
                    raise RuntimeError(
                        f"Invalid value format for attribute '{attr_name}' of type '{type_hint_repr}' declared in "
                        f"'{objname}' object.\nInput value: {input_value or None}"
                    ) from e

        super(SettingsMetaclass, cls).__init__(objname, bases, clsdict)

    @staticmethod
    def __validate_list_annotation(objname: str, attr_name: str, attr_type: Any, type_hint: Any):
        alias_args = get_args(attr_type)
        type_hint_repr = type_hint if type(type_hint) is not type else type_hint.__name__
        if not alias_args:
            raise SettingsValidationException(
                f"Invalid type annotation at '{objname}' class. Attribute '{attr_name}' cannot be declared as '{type_hint_repr}'."
                "\n\t\t -> list annotations should be annotate their contents too as list[str], or list[int], etc."
            )

        has_origin = get_origin(alias_args[0])
        if has_origin:
            raise SettingsValidationException(
                f"Invalid type annotation at '{objname}' class. Attribute '{attr_name}' cannot be declared as '{type_hint_repr}'."
                "\n\t\t -> Union type is not allowed for list type annotation."
            )

        if not all(ta in _ALLOWED_SETTINGS_LIST_TYPES for ta in alias_args):
            raise SettingsValidationException(
                f"Invalid type annotation at '{objname}' class. Attribute '{attr_name}' cannot be declared as '{type_hint_repr}'. "
                f"\n\t\t -> Only one of allowed types {_ALLOWED_SETTINGS_LIST_TYPES_REPR} is permitted. "
                "\n\t\t -> It can be combinable with None to annotate nullable attributes."
            )

    @staticmethod
    def __cast_list(
        objname: str, attr_name: str, value: str | None, type_hint_repr: str, _type: Any
    ) -> list[_AllowedSettingsListTypeAlias] | None:
        if value is None or not value:
            return []

        loaded_value = value
        if type(loaded_value) is not list:
            try:
                loaded_value = json.loads(value)
            except:
                raise SettingsValidationException(
                    f"Invalid value format for attribute '{attr_name}' of type '{type_hint_repr}' declared in "
                    f"'{objname}' object.\nInput value: {value or None}"
                )

        if type(loaded_value) is not list:
            raise SettingsValidationException(
                f"Invalid value type for attribute '{attr_name}' of type '{type_hint_repr}' declared in "
                f"'{objname}' object.\nInput value: {value or None}"
            )

        alias_args = get_args(_type)
        _type = alias_args[0]

        parsed_value = loaded_value
        if _type is Path:
            parsed_value = [Path(item) for item in loaded_value]

        elif _type is bool:
            parsed_value = []
            for item in loaded_value:
                item_lower = str(item).lower()
                if not isinstance(item, (str, int)) or item_lower not in (
                    "true",
                    "false",
                    "y",
                    "n",
                    "yes",
                    "no",
                    "1",
                    "0",
                ):
                    parsed_value.append(item)
                    continue

                parsed_value.append(item_lower in ("true", "y", "yes", "1"))

        elif _type is datetime and value.isnumeric():
            parsed_value.append(datetime.fromtimestamp(float(value), UTC))

        elif _type is date and value.isnumeric():
            parsed_value.append(datetime.fromtimestamp(float(value), UTC).date())

        elif _type is datetime and value.isascii():
            parsed_value.append(fromisoformat_safe(value) or value)

        elif _type is date and value.isascii():
            pre_parsed_value = fromisoformat_safe(value)
            parsed_value.append(pre_parsed_value.date() if pre_parsed_value is not None else value)

        if not any(type(item) is _type for item in parsed_value):
            raise SettingsValidationException(
                f"Invalid value for attribute '{attr_name}' of type '{type_hint_repr}' declared in "
                f"'{objname}' object.\nInput value: {value or None}"
            )

        return loaded_value

    @staticmethod
    def __cast(
        objname: str,
        attr_name: str,
        type_hint_repr: str,
        value: str | None,
        _type: type[_AllowedSettingsTypeAlias],
        nullable: bool,
    ) -> _AllowedSettingsTypeAlias | None:

        if value is None or not value:
            if nullable:
                return None

            else:
                raise SettingsValidationException(
                    f"Invalid value for attribute '{attr_name}' of type '{type_hint_repr}' declared in "
                    f"'{objname}' object. Attribute is not nullable. \nInput value: {value or None}"
                )

        try:
            if type(value) is value:
                return value

            if _type is str:
                return str(value)

            if _type is int and value.isnumeric():
                return int(value.isnumeric())

            if _type is float and value.isnumeric():
                return float(value)

            if _type is bool and value.lower() in ("true", "false", "y", "n", "yes", "no", "1", "0"):
                return value.lower() in ("true", "y", "yes", "1")

            if _type is Path:
                return Path(value)

            if _type is datetime and value.isnumeric():
                return datetime.fromtimestamp(float(value), UTC)

            if _type is date and value.isnumeric():
                return datetime.fromtimestamp(float(value), UTC).date()

            if _type is datetime and value.isascii():
                return fromisoformat_safe(value) or value

            if _type is date and value.isascii():
                parsed_value = fromisoformat_safe(value)
                return parsed_value.date() if parsed_value is not None else value

        except:
            raise SettingsValidationException(
                f"Invalid value format for attribute '{attr_name}' of type '{type_hint_repr}' declared in "
                f"'{objname}' object.\nInput value: {value or None}"
            )

        raise SettingsValidationException(
            f"Invalid value type for attribute '{attr_name}' of type '{type_hint_repr}' declared in "
            f"'{objname}' object.\nInput value: {value or None}"
        )

    @staticmethod
    def __load_secrets_dir(settings_config: SettingsConfig) -> dict[str, str]:
        secrets_dict: dict[str, str] = {}
        secrets_dir_path = Path(settings_config.secrets_dir)
        if not secrets_dir_path.exists():
            return secrets_dict

        for path in secrets_dir_path.iterdir():
            if path.is_dir():
                continue

            secret = path.read_text()
            name = path.name.lower()

            secrets_dict[name] = secret

        return secrets_dict

    @staticmethod
    def __load_env(settings_config: SettingsConfig) -> dict[str, Any]:
        env_file = settings_config.env_file

        env = {
            **{k.lower(): v for k, v in dotenv_values(env_file, interpolate=False).items()},
            **{k.lower(): v for k, v in dict(os.environ).items()},
        }

        return env


class SettingsBase(metaclass=SettingsMetaclass):
    settings_config: SettingsConfig | None = None
