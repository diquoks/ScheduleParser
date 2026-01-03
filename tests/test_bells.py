import pyquoks

import src.schedule_parser
import tests._test_utils


class TestBells(pyquoks.test.TestCase):
    _MODULE_NAME = __name__

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()

        cls._data = tests._test_utils.DataProvider()

    def test_get_bells_variant(self) -> None:
        for weekday in src.schedule_parser.models.Weekday:
            if weekday != src.schedule_parser.models.Weekday.SUNDAY:
                self.assert_type(
                    func_name=self.test_get_bells_variant.__name__,
                    test_data=self._data.get_bells_variant_by_weekday(weekday),
                    test_type=src.schedule_parser.models.BellsVariant,
                )

        self.assert_raises(
            func_name=self.test_get_bells_variant.__name__,
            test_func=self._data.get_bells_variant_by_weekday,
            test_exception=ValueError,
            weekday=src.schedule_parser.models.Weekday.SUNDAY,
        )
