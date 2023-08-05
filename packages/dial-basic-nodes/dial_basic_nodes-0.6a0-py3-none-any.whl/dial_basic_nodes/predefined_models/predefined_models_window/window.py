# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from typing import TYPE_CHECKING, Optional

import dependency_injector.providers as providers
from PySide2.QtCore import Slot
from PySide2.QtWidgets import (
    QCheckBox,
    QDialogButtonBox,
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QVBoxLayout,
    QWidget,
)

from .model import PredefinedModelsModelFactory
from .view import PredefinedModelsViewFactory

if TYPE_CHECKING:
    from PySide2.QtCore import QModelIndex
    from .model import PredefinedModelsModel
    from .view import PredefinedModelsView


class PredefinedModelsWindow(QWidget):
    """
    Window window for selecting between predefined datasets.
    """

    def __init__(
        self,
        model: "PredefinedModelsModel",
        view: "PredefinedModelsView",
        parent: "QWidget" = None,
    ):
        super().__init__(parent)

        self.setWindowTitle("Datasets")

        # Attributes
        self._selected_model = None

        # Setup MVC
        self._model = model
        self._model.setParent(self)
        self._view = view
        self._view.setParent(self)

        self._view.setModel(self._model)

        # Create widgets
        self._name_label = QLabel()
        self._include_top_checkbox = QCheckBox("Include top")

        # Create Layouts
        self._main_layout = QHBoxLayout()
        self._description_layout = QFormLayout()

        # Main layout
        self.setLayout(self._main_layout)

        # Right side (Description)

        self._description_layout.addRow("Name:", self._name_label)
        self._description_layout.addWidget(self._include_top_checkbox)

        # Extra vertical layout for window button_box widget
        right_layout = QVBoxLayout()
        right_layout.addLayout(self._description_layout)

        # Add widgets to main layout
        self._main_layout.addWidget(self._view)
        self._main_layout.addLayout(right_layout)

        # // Connections
        self._view.activated.connect(self._selected_loader_changed)

    def selected_model(self) -> Optional["TTVSetsLoader"]:
        """
        Return the loaded currently selected by the Window.
        """
        return self._selected_model

    @Slot("QModelIndex")
    def _selected_loader_changed(self, index: "QModelIndex"):
        """
        Slot called when a user clicks on any list item.
        """
        self._selected_model = index.internalPointer()

        self._update_description(self._selected_model)

    @Slot("TTVSetsLoader")
    def _update_description(self, selected_model):
        """
        Update the description on the right widget after selecting a new TTVSetsLoader.
        """
        self._name_label.setText(selected_model["name"])
        # self._brief_label.setText(ttv_sets_loader.brief)
        # self._types_label.setText(
        #     ", ".join([str(ttv_sets_loader.x_type), str(ttv_sets_loader.y_type)])
        # )

    def __reduce__(self):
        return (PredefinedModelsWindow, (self._model, self._view))


PredefinedModelsWindowFactory = providers.Factory(
    PredefinedModelsWindow,
    model=PredefinedModelsModelFactory,
    view=PredefinedModelsViewFactory,
)
