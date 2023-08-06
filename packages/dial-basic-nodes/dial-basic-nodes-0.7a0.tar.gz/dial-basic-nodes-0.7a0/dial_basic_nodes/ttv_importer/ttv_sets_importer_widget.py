# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

import os

import dependency_injector.providers as providers
from dial_core.datasets import TTVSets
from dial_core.datasets.io import (
    CategoricalImgDatasetIO,
    DatasetIORegistry,
    NpzDatasetIO,
    TTVSetsIO,
)
from dial_core.utils import log
from PySide2.QtCore import QSize, Signal
from PySide2.QtWidgets import (
    QComboBox,
    QDialogButtonBox,
    QFileDialog,
    QFormLayout,
    QFrame,
    QHBoxLayout,
    QLineEdit,
    QPushButton,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from .datatype_selector import DatatypeSelectorFactory
from .formats_widgets import CategoricalImagesWidgetFactory, NpzWidgetFactory

LOGGER = log.get_logger(__name__)

FORMAT_TO_WIDGET = {
    NpzDatasetIO.Label: NpzWidgetFactory,
    CategoricalImgDatasetIO.Label: CategoricalImagesWidgetFactory,
}


class TTVSetsImporterWidget(QWidget):
    ttv_updated = Signal(TTVSets)

    def __init__(
        self, format_to_widget, parent: "QWidget" = None,
    ):
        super().__init__(parent)

        # Components
        self._ttv = None

        # Maps a  with its respective Widget
        self._format_to_widget = format_to_widget

        self._stacked_widgets = QStackedWidget()

        self._name_textbox = QLineEdit("Unnamed")

        self._formatter_selector = QComboBox()
        for (dataset_io_name, widget_factory) in self._format_to_widget.items():
            self._formatter_selector.addItem(
                dataset_io_name, getattr(DatasetIORegistry, dataset_io_name)
            )
            self._stacked_widgets.addWidget(self._format_to_widget[dataset_io_name]())

        def horizontal_line():
            line = QFrame()
            line.setFrameShape(QFrame.HLine)
            line.setFrameShadow(QFrame.Sunken)
            line.setFixedHeight(2)
            line.setContentsMargins(0, 30, 0, 0)
            return line

        self._x_datatype_selector = DatatypeSelectorFactory(title="X (Input) Datatype")
        self._y_datatype_selector = DatatypeSelectorFactory(title="Y (Output) Datatype")

        datatypes_layout = QHBoxLayout()
        datatypes_layout.addWidget(self._x_datatype_selector)
        datatypes_layout.addWidget(self._y_datatype_selector)

        self._info_layout = QFormLayout()
        self._info_layout.addRow("Name", self._name_textbox)
        self._info_layout.addRow("Format", self._formatter_selector)

        self._main_layout = QVBoxLayout()
        self._main_layout.addLayout(self._info_layout)
        self._main_layout.addWidget(horizontal_line())
        self._main_layout.addWidget(self._stacked_widgets)
        self._main_layout.addWidget(horizontal_line())
        self._main_layout.addLayout(datatypes_layout)

        self._load_ttv_from_file_button = QPushButton("Load from file...")
        self._load_ttv_from_file_button.clicked.connect(self._load_ttv_from_file)

        self._update_ttv_button = QPushButton("Load TTV")
        self._update_ttv_button.clicked.connect(self._update_ttv)

        self._button_box = QDialogButtonBox()
        self._button_box.addButton(
            self._load_ttv_from_file_button, QDialogButtonBox.ResetRole
        )
        self._button_box.addButton(self._update_ttv_button, QDialogButtonBox.ApplyRole)

        self._main_layout.addWidget(self._button_box)

        self.setLayout(self._main_layout)

        self._formatter_selector.currentIndexChanged[int].connect(
            lambda i: self._stacked_widgets.setCurrentIndex(i)
        )

    def get_ttv(self) -> "TTVSets":
        return self._ttv

    def _update_ttv(self):
        self._ttv = self._stacked_widgets.currentWidget().load_ttv(
            self._name_textbox.text(),
            self._x_datatype_selector.selected_datatype,
            self._y_datatype_selector.selected_datatype,
        )

        self.ttv_updated.emit(self._ttv)

    def _load_ttv_from_file(self):
        print("Loading from file...")

        description_file_path = QFileDialog.getOpenFileName(
            self, "Open TTV .json file"
        )[0]

        if description_file_path:
            LOGGER.debug("Loading %s...", description_file_path)

            ttv_dir = os.path.dirname(description_file_path)
            ttv_description = TTVSetsIO.load_ttv_description(description_file_path)

            # Update name
            self._name_textbox.setText(ttv_description["name"])

            # Pick the new formatter
            formatter_idx = self._formatter_selector.findText(ttv_description["format"])

            if formatter_idx != -1:
                self._formatter_selector.setCurrentIndex(formatter_idx)
                self._selected_index_changed(formatter_idx)

            # TODO: Cover case when "train" is null
            self._x_datatype_selector.change_current_datatype(
                ttv_description["train"]["x_type"]
            )
            self._y_datatype_selector.change_current_datatype(
                ttv_description["train"]["y_type"]
            )

            self._stacked_widgets.currentWidget().update_widgets(
                ttv_dir, ttv_description
            )

            self._update_ttv()

        else:
            LOGGER.debug("Loading cancelled")

    def _selected_index_changed(self, index: int):
        self._stacked_widgets.setCurrentIndex(index)

    def sizeHint(self) -> "QSize":
        """Optimal size of the widget."""
        return QSize(450, 150)

    def __reduce__(self):
        return (
            TTVSetsImporterWidget,
            (self._ttv_sets_dialog, None),
        )


TTVSetsImporterWidgetFactory = providers.Factory(
    TTVSetsImporterWidget, format_to_widget=FORMAT_TO_WIDGET,
)
