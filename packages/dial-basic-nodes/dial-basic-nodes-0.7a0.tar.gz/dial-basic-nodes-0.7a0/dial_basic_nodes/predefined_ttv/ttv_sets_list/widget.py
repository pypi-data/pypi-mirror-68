# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from typing import TYPE_CHECKING, Optional

import dependency_injector.providers as providers
from dial_core.datasets.io import TTVSetsLoader
from PySide2.QtCore import QSize, Signal, Slot
from PySide2.QtWidgets import QFormLayout, QHBoxLayout, QLabel, QVBoxLayout, QWidget

from .model import PredefinedTTVSetsListModelFactory, TTVSetsListModelFactory
from .view import TTVSetsListViewFactory

if TYPE_CHECKING:
    from PySide2.QtCore import QModelIndex
    from .model import DatasetsListModel
    from .view import DatasetsListView


class TTVSetsListWidget(QWidget):
    """
    Window for selecting between predefined datasets.
    """

    selected_ttv_loader_changed = Signal(TTVSetsLoader)

    def __init__(
        self,
        model: "DatasetsListModel",
        view: "DatasetsListView",
        parent: "QWidget" = None,
    ):
        super().__init__(parent)

        # Attributes
        self._ttv_sets_loader: Optional["TTVSetsLoader"] = None

        # Setup MVC
        self._model = model
        self._model.setParent(self)
        self._view = view
        self._view.setParent(self)

        self._view.setModel(self._model)

        # Create widgets
        self._name_label = QLabel()
        self._brief_label = QLabel()
        self._types_label = QLabel()

        # Create Layouts
        self._main_layout = QHBoxLayout()
        self._description_layout = QFormLayout()

        # Setup UI
        self._setup_ui()

        self._view.activated.connect(self._selected_loader_changed)

    def selected_loader(self) -> Optional["TTVSetsLoader"]:
        """
        Return the loaded currently selected by the widget.
        """
        return self._ttv_sets_loader

    def selected_ttv(self) -> Optional["TTVSets"]:
        return self._ttv_sets_loader.load() if self._ttv_sets_loader else None

    def _setup_ui(self):
        # Main layout
        self.setLayout(self._main_layout)

        # Right side (Description)

        self._description_layout.addRow("Name", self._name_label)
        self._description_layout.addRow("Brief", self._brief_label)
        self._description_layout.addRow("Data types:", self._types_label)

        right_layout = QVBoxLayout()
        right_layout.addLayout(self._description_layout)

        # Add widgets to main layout
        self._main_layout.addWidget(self._view)
        self._main_layout.addLayout(right_layout)

    @Slot("QModelIndex")
    def _selected_loader_changed(self, index: "QModelIndex"):
        """
        Slot called when a user clicks on any list item.
        """
        self._ttv_sets_loader = index.internalPointer()

        self.selected_ttv_loader_changed.emit(self._ttv_sets_loader)
        print("Cahngingc")

        self._update_description(self._ttv_sets_loader)

    @Slot("TTVSetsLoader")
    def _update_description(self, ttv_sets_loader: "TTVSetsLoader"):
        """
        Update the description on the right widget after selecting a new TTVSetsLoader.
        """
        self._name_label.setText(ttv_sets_loader.name)
        self._brief_label.setText(ttv_sets_loader.brief)
        self._types_label.setText(
            ", ".join([str(ttv_sets_loader.x_type), str(ttv_sets_loader.y_type)])
        )

    def sizeHint(self) -> "QSize":
        """Optimal size of the widget."""
        return QSize(450, 150)

    def __reduce__(self):
        return (TTVSetsListWidget, (self._model, self._view))


TTVSetsListWidgetFactory = providers.Factory(
    TTVSetsListWidget, model=TTVSetsListModelFactory, view=TTVSetsListViewFactory
)

PredefinedTTVSetsListWidgetFactory = providers.Factory(
    TTVSetsListWidget,
    model=PredefinedTTVSetsListModelFactory,
    view=TTVSetsListViewFactory,
)
