from __future__ import annotations
import pyquoks
import models


# region Providers

class DataProvider(pyquoks.data.DataProvider):
    _OBJECTS = {
        "bells": models.BellsScheduleContainer
    }

    bells: models.BellsScheduleContainer

# endregion
