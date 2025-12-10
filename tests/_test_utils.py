import enum

import pyquoks

import schedule_parser


# region models.py

class BellsVariants(enum.Enum):
    Monday = 0
    Wednesday = 1
    Other = 2


# endregion

# region data.py

class DataProvider(pyquoks.data.DataManager):
    _OBJECTS = {
        "bells": list[schedule_parser.models.BellsVariant],
    }

    _PATH = pyquoks.utils.get_path("resources/data/")

    bells: list[schedule_parser.models.BellsVariant]

    def get_bells_variant_by_weekday(
            self,
            weekday: schedule_parser.models.Weekday
    ) -> schedule_parser.models.BellsVariant:
        match weekday:
            case schedule_parser.models.Weekday.MONDAY:
                return self.bells[BellsVariants.Monday.value]
            case schedule_parser.models.Weekday.WEDNESDAY:
                return self.bells[BellsVariants.Wednesday.value]
            case schedule_parser.models.Weekday.TUESDAY | schedule_parser.models.Weekday.THURSDAY | \
                 schedule_parser.models.Weekday.FRIDAY | schedule_parser.models.Weekday.SATURDAY:
                return self.bells[BellsVariants.Other.value]
            case schedule_parser.models.Weekday.SUNDAY:
                raise ValueError

# endregion
