import enum
import typing

import pyquoks


# region Enums

class Weekday(enum.Enum):
    MONDAY = 0
    TUESDAY = 1
    WEDNESDAY = 2
    THURSDAY = 3
    FRIDAY = 4
    SATURDAY = 5
    SUNDAY = 6

    @staticmethod
    def from_string(string: str) -> Weekday:
        match string.lower():
            case "понедельник":
                return Weekday.MONDAY
            case "вторник":
                return Weekday.TUESDAY
            case "среда":
                return Weekday.WEDNESDAY
            case "четверг":
                return Weekday.THURSDAY
            case "пятница":
                return Weekday.FRIDAY
            case "суббота":
                return Weekday.SATURDAY
            case "воскресенье":
                return Weekday.SUNDAY
            case _:
                raise ValueError(f"Unknown weekday: {string!r}")


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
    def formatted_room(self) -> str:
        if self.room.isdigit():
            return f"{self.room} к."
        else:
            return self.room

    @property
    def is_empty(self) -> bool:
        return not bool(self.lecturer and self.room and self.subject)

    @property
    def readable(self) -> str:
        if self.is_empty:
            raise ValueError("Period is empty!")
        else:
            return " | ".join([
                " ".join(i for i in [
                    f"{self.number}.",
                    f"({self.subgroup})" if self.subgroup else "",
                    self.subject,
                ] if i),
                self.formatted_room,
            ])

    def is_same_but_metadata(self, period: PeriodModel) -> bool:
        return (
            self.number,
            self.subgroup,
        ) == (
            period.number,
            period.subgroup,
        )

    def is_same_but_subgroup(self, period: PeriodModel) -> bool:
        return (
            self.lecturer,
            self.number,
            self.room,
            self.subject,
        ) == (
            period.lecturer,
            period.number,
            period.room,
            period.subject,
        )


class DayScheduleContainer(pyquoks.models.Container):
    _ATTRIBUTES = {
        "weekday",
    }

    _DATA = {
        "schedule": PeriodModel,
    }

    schedule: list[PeriodModel]
    weekday: int

    @property
    def is_empty(self) -> bool:
        return not bool(self.schedule)


class WeekScheduleContainer(pyquoks.models.Container):
    _ATTRIBUTES = {
        "parity",
    }

    _DATA = {
        "schedule": DayScheduleContainer,
    }

    parity: bool
    schedule: list[DayScheduleContainer]

    def get_day_schedule_by_weekday(self, weekday: Weekday) -> DayScheduleContainer | None:
        try:
            return list(
                filter(
                    lambda schedule: schedule.weekday == weekday.value,
                    self.schedule,
                )
            )[0]
        except IndexError:
            raise ValueError(f"Could not find schedule for weekday: {weekday!r}")


class GroupScheduleContainer(pyquoks.models.Container):
    _ATTRIBUTES = {
        "group",
    }

    _DATA = {
        "schedule": WeekScheduleContainer,
    }

    group: str
    schedule: list[WeekScheduleContainer]

    def get_week_schedule_by_parity(self, parity: bool) -> WeekScheduleContainer | None:
        try:
            return list(
                filter(
                    lambda schedule: schedule.parity == parity,
                    self.schedule,
                )
            )[0]
        except IndexError:
            raise ValueError(f"Could not find schedule for parity: {parity!r}")


class GroupSchedulesListing(pyquoks.models.Listing):
    _DATA = {
        "schedule": GroupScheduleContainer,
    }

    schedule: list[GroupScheduleContainer]

    @staticmethod
    def from_iterable(iterable: typing.Iterable[GroupScheduleContainer]) -> GroupSchedulesListing:
        def _get_model_data(model: GroupScheduleContainer) -> dict:
            return model._data

        return GroupSchedulesListing(
            data=list(
                map(
                    _get_model_data,
                    iterable,
                )
            ),
        )

    def get_group_schedule(self, group: str) -> GroupScheduleContainer | None:
        try:
            return list(
                filter(
                    lambda schedule: schedule.group == group,
                    self.schedule,
                )
            )[0]
        except IndexError:
            raise ValueError(f"Could not find schedule for group: {group!r}")


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


class SubstitutionsListing(pyquoks.models.Listing):
    _DATA = {
        "substitutions": SubstitutionModel,
    }

    substitutions: list[SubstitutionModel]

    @staticmethod
    def from_iterable(iterable: typing.Iterable[SubstitutionModel]) -> SubstitutionsListing:
        def _get_model_data(model: SubstitutionModel) -> dict:
            return model._data

        return SubstitutionsListing(
            data=list(
                map(
                    _get_model_data,
                    iterable,
                )
            ),
        )

    def get_substitutions_by_group(self, group: str) -> list[SubstitutionModel]:
        return list(
            filter(
                lambda substitution: substitution.group == group,
                self.substitutions,
            )
        )


class BellsVariantContainer(pyquoks.models.Container):
    _DATA = {
        "bells": str,
    }

    bells: list[str]

    def format_period(self, period: PeriodModel) -> str:
        return " | ".join([
            self.bells[period.number],
            period.readable,
        ])


class BellsScheduleListing(pyquoks.models.Listing):
    _DATA = {
        "variants": BellsVariantContainer,
    }

    variants: list[BellsVariantContainer]

    def get_variant_by_weekday(
            self,
            weekday: Weekday,
    ) -> BellsVariantContainer:
        raise NotImplementedError()

# endregion
