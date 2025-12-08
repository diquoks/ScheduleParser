import datetime

import openpyxl
import pyquoks

import schedule_parser


class TestUtils(pyquoks.test.TestCase):
    _MODULE_NAME = __name__

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()

        cls._substitutions_names = [
            "substitutions",
            "substitutions_incorrect",
            "substitutions_old",
        ]

        cls._group = "СИСАД 24-01"
        cls._schedule_with_substitutions = {
            "08_11_25": "",
            "18_11_25": (
                "0. Разг. о важном | 45 к.\n"
                "1. ААС | 34 к.\n"
                "2. Операц. СиС | 34 к.\n"
                "3. ТФУПД | 44 к.\n"
                "4. Иностр. яз. | 1 к."
            ),
            "25_11_25": (
                "0. Разг. о важном | 45 к.\n"
                "1. (1) Иностр. яз. | 1 к.\n"
                "1. (2) Иностр. яз. | 23 к.\n"
                "2. Комп. сети (П) | 45 к.\n"
                "3. ААС | 34 к.\n"
                "4. Операц. СиС | 34 к."
            ),
            "28_11_25": (
                "1. Кл. час | 45 к.\n"
                "2. Комп. сети (Л) | 45 к.\n"
                "3. Комп. сети (П) | 45 к.\n"
                "4. Элементы ВМ | 40 к.\n"
                "5. Элементы ВМ | э/о"
            ),
            "29_11_25": "",
            "02_12_25": (
                "1. Разг. о важном | 45 к.\n"
                "2. Комп. сети (Л) | 33 к.\n"
                "3. ТФУПД | 11 к.\n"
                "4. (1) Иностр. яз. | 1 к.\n"
                "4. (2) Иностр. яз. | 23 к."
            ),
            "06_12_25": (
                "0. Кл. час | 45 к.\n"
                "1. Основы проектирования баз данных | 34 к.\n"
                "2. Основы проектирования баз данных | 34 к.\n"
                "3. ТФУПД | 44 к."
            ),
        }

    def test_parse_schedule(self):
        workbook = openpyxl.load_workbook(
            filename=pyquoks.utils.get_path("resources/tables/schedule.xlsx"),
        )

        for group in list(schedule_parser.utils.parse_schedule(workbook.worksheets[0])):
            self.assert_type(
                func_name=self.test_parse_schedule.__name__,
                test_data=group,
                test_type=schedule_parser.models.GroupScheduleContainer,
                message="objects in parsed schedules list",
            )

    def test_parse_substitutions(self):
        for name in self._substitutions_names:
            workbook = openpyxl.load_workbook(
                filename=pyquoks.utils.get_path(f"resources/tables/{name}.xlsx"),
            )

            for substitution in list(schedule_parser.utils.parse_substitutions(workbook.worksheets[0])):
                self.assert_type(
                    func_name=self.test_parse_substitutions.__name__,
                    test_data=substitution,
                    test_type=schedule_parser.models.SubstitutionModel,
                    message=f"({name}) objects in parsed substitutions list",
                )

    def test_schedule_with_substitutions(self):
        workbook_schedule = openpyxl.load_workbook(
            filename=pyquoks.utils.get_path("resources/tables/schedule.xlsx"),
        )

        for name, correct_schedule in self._schedule_with_substitutions.items():
            workbook_substitutions = openpyxl.load_workbook(
                filename=pyquoks.utils.get_path(f"resources/tables/substitutions_{name}.xlsx"),
            )

            current_date = datetime.datetime.strptime(name, "%d_%m_%y")

            current_schedule = schedule_parser.utils.get_schedule_with_substitutions(
                schedule=schedule_parser.models.GroupSchedulesListing(
                    data=schedule_parser.utils._get_data_from_models_iterable(
                        models_iterable=schedule_parser.utils.parse_schedule(
                            worksheet=workbook_schedule.worksheets[0],
                        ),
                    ),
                ),
                substitutions=schedule_parser.models.SubstitutionsListing(
                    data=schedule_parser.utils._get_data_from_models_iterable(
                        models_iterable=schedule_parser.utils.parse_substitutions(
                            worksheet=workbook_substitutions.worksheets[0],
                        ),
                    ),
                ),
                group=self._group,
                date=current_date,
            )

            self.assert_equal(
                func_name=self.test_schedule_with_substitutions.__name__,
                test_data="\n".join(
                    map(
                        lambda period: period.readable,
                        current_schedule,
                    ),
                ),
                test_expected=correct_schedule,
                message=f"({name}) compare parsed schedule with correct one",
            )
