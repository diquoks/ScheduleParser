from __future__ import annotations
import enum
import pyquoks


# region Enums

class Weekdays(enum.Enum):
    Monday = 0
    Tuesday = 1
    Wednesday = 2
    Thursday = 3
    Friday = 4
    Saturday = 5


class BellsVariants(enum.Enum):
    Monday = 0
    Wednesday = 1
    Other = 2


# endregion

# region Models & Containers

class BellsVariantContainer(pyquoks.models.Container):
    _DATA = {
        "bells": str,
    }

    bells: list[str]


class BellsScheduleContainer(pyquoks.models.Container):
    _DATA = {
        "variants": BellsVariantContainer,
    }

    variants: list[BellsVariantContainer]

    def get_variant_by_weekday(self, weekday: Weekdays) -> BellsVariantContainer:
        match weekday:
            case Weekdays.Monday:
                return self.variants[BellsVariants.Monday.value]
            case Weekdays.Wednesday:
                return self.variants[BellsVariants.Wednesday.value]
            case Weekdays.Tuesday | Weekdays.Thursday | Weekdays.Friday | Weekdays.Saturday:
                return self.variants[BellsVariants.Other.value]

# endregion
