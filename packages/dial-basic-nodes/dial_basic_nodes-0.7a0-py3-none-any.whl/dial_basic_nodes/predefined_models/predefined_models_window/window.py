# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from typing import TYPE_CHECKING

import dependency_injector.providers as providers
from PySide2.QtCore import Signal, Slot
from PySide2.QtWidgets import QHBoxLayout, QWidget
from tensorflow.keras import Model

from .model import PredefinedModelsModelFactory
from .view import PredefinedModelsViewFactory

if TYPE_CHECKING:
    from PySide2.QtCore import QModelIndex
    from .model import PredefinedModelsModel
    from .view import PredefinedModelsView


class PredefinedModelsWindow(QWidget):
    """Window window for selecting between predefined datasets."""

    selected_model_changed = Signal(Model)

    def __init__(
        self,
        model: "PredefinedModelsModel",
        view: "PredefinedModelsView",
        parent: "QWidget" = None,
    ):
        super().__init__(parent)

        self.setWindowTitle("Datasets")

        # Components
        self._selected_model = None

        # Setup MVC Widgets
        self._model = model
        self._model.setParent(self)
        self._view = view
        self._view.setParent(self)

        self._view.setModel(self._model)

        # Main layout
        self._main_layout = QHBoxLayout()
        self._main_layout.addWidget(self._view)
        self.setLayout(self._main_layout)

        # // Connections
        self._view.activated.connect(self._new_model_selected)

    def get_selected_model(self):
        """
        Return the model currently selected on this widget's list.
        """
        return self._selected_model

    @Slot("QModelIndex")
    def _new_model_selected(self, index: "QModelIndex"):
        """
        Slot called when a user clicks on any list item.
        """
        self._selected_model = index.internalPointer()

        self.selected_model_changed.emit(self._selected_model)

    def __reduce__(self):
        return (PredefinedModelsWindow, (self._model, self._view))


PredefinedModelsWindowFactory = providers.Factory(
    PredefinedModelsWindow,
    model=PredefinedModelsModelFactory,
    view=PredefinedModelsViewFactory,
)
