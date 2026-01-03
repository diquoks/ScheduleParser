import enum

import pyquoks

import src.schedule_parser


# region models.py

class BellsType(enum.Enum):
    MONDAY = 0
    WEDNESDAY = 1
    OTHER = 2


# endregion

# region data.py

class DataProvider(pyquoks.data.DataManager):
    _PATH = pyquoks.utils.get_path("tests/resources/data/")

    bells: list[src.schedule_parser.models.BellsVariant]

    def get_bells_variant_by_weekday(
            self,
            weekday: src.schedule_parser.models.Weekday
    ) -> src.schedule_parser.models.BellsVariant:
        match weekday:
            case src.schedule_parser.models.Weekday.MONDAY:
                return self.bells[BellsType.MONDAY.value]
            case src.schedule_parser.models.Weekday.WEDNESDAY:
                return self.bells[BellsType.WEDNESDAY.value]
            case src.schedule_parser.models.Weekday.TUESDAY | src.schedule_parser.models.Weekday.THURSDAY | \
                 src.schedule_parser.models.Weekday.FRIDAY | src.schedule_parser.models.Weekday.SATURDAY:
                return self.bells[BellsType.OTHER.value]
            case src.schedule_parser.models.Weekday.SUNDAY:
                raise ValueError

# endregion
