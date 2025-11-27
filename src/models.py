from __future__ import annotations

import enum

import pyquoks


# region Enums

class Weekdays(enum.Enum):
    MONDAY = 1
    TUESDAY = 2
    WEDNESDAY = 3
    THURSDAY = 4
    FRIDAY = 5
    SATURDAY = 6
    SUNDAY = 7


# endregion

# region Models & Containers

class PeriodModel(pyquoks.models.Model):
    _ATTRIBUTES = {
        "lecturer",
        "number",
        "room",
        "subgroup",
        "subject",
    }

    lecturer: str
    number: int
    room: str
    subgroup: int
    subject: str

    @property
    def is_empty(self) -> bool:
        return not bool(self.lecturer and self.room and self.subject)


class SubstitutionModel(pyquoks.models.Model):
    _ATTRIBUTES = {
        "group",
    }

    _OBJECTS = {
        "period": PeriodModel,
        "substitution": PeriodModel,
    }

    group: str
    period: PeriodModel
    substitution: PeriodModel

    @property
    def number(self) -> int:
        return self.substitution.number

    @property
    def subgroup(self) -> int:
        return self.substitution.subgroup


class BellsVariantContainer(pyquoks.models.Container):
    _DATA = {
        "bells": str,
    }

    bells: list[str]

# endregion
