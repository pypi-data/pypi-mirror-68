# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from typing import TYPE_CHECKING

import dependency_injector.providers as providers
from dial_core.datasets import Dataset
from PySide2.QtCore import Signal
from PySide2.QtWidgets import QVBoxLayout, QWidget

from .dataset_table_model import DatasetTableModelFactory
from .dataset_table_view import DatasetTableViewFactory

if TYPE_CHECKING:
    from .dataset_table_model import DatasetTableModel
    from .dataset_table_view import DatasetTableView


class DatasetTableWidget(QWidget):
    dataset_loaded = Signal(Dataset)

    def __init__(
        self,
        view: "DatasetTableView",
        model: "DatasetTableModel",
        parent: "QWidget" = None,
    ):
        super().__init__(parent)

        # Componentes
        self._dataset_table_model = model
        self._dataset_table_view = view
        self._dataset_table_view.setModel(self._dataset_table_model)

        # Widgets
        self._main_layout = QVBoxLayout()
        self._main_layout.setContentsMargins(0, 0, 0, 0)

        self._main_layout.addWidget(self._dataset_table_view)

        self.setLayout(self._main_layout)

        # Connections
        self._dataset_table_model.dataset_loaded.connect(
            lambda dataset: self.dataset_loaded.emit(dataset)
        )

    @property
    def dataset(self):
        """Returns the dataset loaded on the model."""
        return self._dataset_table_model.dataset

    def load_dataset(self, dataset: "Dataset"):
        """Loads a new dataset onto the model."""
        self._dataset_table_model.load_dataset(dataset)

    def __getstate__(self):
        return {"dataset": self._dataset_table_model.dataset}

    def __setstate__(self, new_state):
        self.load_dataset(new_state["dataset"])


DatasetTableWidgetFactory = providers.Factory(
    DatasetTableWidget, model=DatasetTableModelFactory, view=DatasetTableViewFactory
)
