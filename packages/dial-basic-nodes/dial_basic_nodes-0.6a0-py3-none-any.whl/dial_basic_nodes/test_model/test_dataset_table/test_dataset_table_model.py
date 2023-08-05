# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from enum import IntEnum
from typing import Any, List

import dependency_injector.providers as providers
# from dial_core.datasets import Dataset
from PySide2.QtCore import QObject, Qt

from dial_basic_nodes.utils.dataset_table import DatasetTableModel


class TestDatasetTableModel(DatasetTableModel):
    PredictionResultRole = Qt.UserRole + 2

    class ColumnLabel(IntEnum):
        Input = 0
        Prediction = 1
        Output = 2

    def __init__(self, parent: "QObject" = None):
        super().__init__(parent)

        self._prediction_data = []

        self._role_map[self.PredictionResultRole] = self._prediction_result_role

    def set_predict_values(self, prediction_data: List[Any]):
        type_of_prediction = self._type_of(self.ColumnLabel.Prediction)

        self._prediction_data = [
            type_of_prediction.display(
                type_of_prediction.convert_to_expected_format(value)
            )
            for value in prediction_data
        ]

    def clear(self):
        super().clear()

        self._prediction_data.clear()
        self._prediction_data = []

    def _data_of(self, column: int):
        if column == self.ColumnLabel.Input:
            return self._cached_data[0]

        elif column == self.ColumnLabel.Output:
            return self._cached_data[1]

        elif column == self.ColumnLabel.Prediction:
            return self._prediction_data

    def _type_of(self, column: int):
        if column == self.ColumnLabel.Input:
            return self._types[0]

        elif column == self.ColumnLabel.Output:
            return self._types[1]

        elif column == self.ColumnLabel.Prediction:
            return self._types[1]

    def _prediction_result_role(self, row: int, column: int) -> bool:
        try:
            return (
                self._data_of(self.ColumnLabel.Prediction)[row]
                == self._data_of(self.ColumnLabel.Output)[row]
            )

        except IndexError:
            return None


TestDatasetTableModelFactory = providers.Factory(TestDatasetTableModel)
