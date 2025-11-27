from __future__ import annotations

import enum

import pyquoks

import models


# region models.py

class BellsVariants(enum.Enum):
    Monday = 0
    Wednesday = 1
    Other = 2


class BellsScheduleContainer(pyquoks.models.Container):
    _DATA = {
        "variants": models.BellsVariantContainer,
    }

    variants: list[models.BellsVariantContainer]

    def get_variant_by_weekday(
            self,
            weekday: models.Weekdays,
    ) -> models.BellsVariantContainer:
        match weekday:
            case models.Weekdays.MONDAY:
                return self.variants[BellsVariants.Monday.value]
            case models.Weekdays.WEDNESDAY:
                return self.variants[BellsVariants.Wednesday.value]
            case models.Weekdays.TUESDAY | models.Weekdays.THURSDAY | models.Weekdays.FRIDAY | models.Weekdays.SATURDAY:
                return self.variants[BellsVariants.Other.value]
            case models.Weekdays.SUNDAY:
                raise ValueError


# endregion

# region data.py

class DataProvider(pyquoks.data.DataProvider):
    _OBJECTS = {
        "bells": BellsScheduleContainer
    }

    _PATH = pyquoks.utils.get_path("resources/data/")

    bells: BellsScheduleContainer

# endregion
