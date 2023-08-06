# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from typing import Any, List

import dependency_injector.providers as providers
from PySide2.QtWidgets import QWidget

from dial_basic_nodes.utils.dataset_table import (
    DatasetTableView,
    DatasetTableViewFactory,
    DatasetTableWidget,
)

from .test_dataset_table_item_delegate import TestDatasetTableItemDelegate
from .test_dataset_table_model import (
    TestDatasetTableModel,
    TestDatasetTableModelFactory,
)


class TestDatasetTableWidget(DatasetTableWidget):
    def __init__(
        self,
        view: "DatasetTableView",
        model: "TestDatasetTableModel",
        parent: "QWidget" = None,
    ):
        super().__init__(view, model, parent)

        self._dataset_table_view.setItemDelegate(TestDatasetTableItemDelegate())

    def set_predict_values(self, prediction_data: List[Any]):
        self._dataset_table_model.set_predict_values(prediction_data)


TestDatasetTableWidgetFactory = providers.Factory(
    TestDatasetTableWidget,
    view=DatasetTableViewFactory,
    model=TestDatasetTableModelFactory,
)
