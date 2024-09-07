from typing import Any

__all__ = [
    "Criteria",
]


class Criteria: ...


class BooleanCriteria(Criteria):
    field: Any
    value: Any

    def __init__(self, field, value):
        super().__init__()
        self.field = field
        self.value = value

    def __and__(self, other):
        return AndCriteria(self, other)

    def __or__(self, other):
        return OrCriteria(self, other)

    def __xor__(self, other):
        return XorCriteria(self, other)

    def __invert__(self):
        return NotCriteria(self)


class EqCriteria(BooleanCriteria):
    def __str__(self):
        return f"{self.field} == '{self.value}'"


class NeCriteria(BooleanCriteria):
    def __str__(self):
        return f"{self.field} != '{self.value}'"


class LtCriteria(BooleanCriteria):
    def __str__(self):
        return f"{self.field} < '{self.value}'"


class LeCriteria(BooleanCriteria):
    def __str__(self):
        return f"{self.field} <= '{self.value}'"


class GtCriteria(BooleanCriteria):
    def __str__(self):
        return f"{self.field} > '{self.value}'"


class GeCriteria(BooleanCriteria):
    def __str__(self):
        return f"{self.field} >= '{self.value}'"


class InCriteria(BooleanCriteria):
    def __str__(self):
        return f"{self.field} in '{self.value}'"


class LikeCriteria(BooleanCriteria):
    def __str__(self):
        return f"{self.field} like '{self.value}'"


class NotLikeCriteria(BooleanCriteria):
    def __str__(self):
        return f"{self.field} not_like '{self.value}'"


class BooleanClauseList(Criteria):
    clause_list: tuple["BooleanClauseList", ...]

    def __init__(self, *clause_list):
        super().__init__()
        self.clause_list = clause_list

    def __and__(self, other):
        return AndCriteria(self, other)

    def __or__(self, other):
        return OrCriteria(self, other)

    def __xor__(self, other):
        return XorCriteria(self, other)

    def __invert__(self):
        return NotCriteria(self)


class AndCriteria(BooleanClauseList):
    def __and__(self, other):
        if isinstance(other, AndCriteria):
            self.clause_list += other.clause_list
        else:
            self.clause_list += (other,)

        return self

    def __str__(self):
        return " & ".join([str(clause) for clause in self.clause_list])


class OrCriteria(BooleanClauseList):
    def __or__(self, other):
        if isinstance(other, OrCriteria):
            self.clause_list += other.clause_list
        else:
            self.clause_list += (other,)
        return self

    def __str__(self):
        return " | ".join([str(clause) for clause in self.clause_list])


class NotCriteria(BooleanClauseList):
    def __str__(self):
        return f"~ {self.clause_list[0]}"


class XorCriteria(BooleanClauseList):
    def __str__(self):
        return f"{self.clause_list[0]} ^ '{self.clause_list[1]}'"
