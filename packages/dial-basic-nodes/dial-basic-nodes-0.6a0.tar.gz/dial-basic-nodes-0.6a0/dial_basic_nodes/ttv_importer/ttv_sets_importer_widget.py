# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

import dependency_injector.providers as providers
from dial_core.datasets import TTVSets
from dial_core.datasets.io import DatasetIORegistrySingleton, TTVSetsIO
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
    DatasetIORegistrySingleton().providers["NpzDatasetIO"]: NpzWidgetFactory,
    DatasetIORegistrySingleton().providers[
        "CategoricalImgDatasetIO"
    ]: CategoricalImagesWidgetFactory,
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
        for (dataset_io, widget_factory) in self._format_to_widget.items():
            self._formatter_selector.addItem(dataset_io.__name__, dataset_io)
            self._stacked_widgets.addWidget(self._format_to_widget[dataset_io]())

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

        self._update_ttv_button = QPushButton("Update TTV")
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

        ttv_dir = QFileDialog.getExistingDirectory(self, "Open TTV Directory")

        if ttv_dir:
            LOGGER.debug("Loading %s...", ttv_dir)

            ttv_description = TTVSetsIO.get_ttv_description(ttv_dir)

            # Update widgets with the description values

            self._name_textbox.setText(ttv_description["name"])

            formatter_idx = self._formatter_selector.findText(ttv_description["format"])
            print(formatter_idx)

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

            self._ttv = self._stacked_widgets.currentWidget().load_ttv_from_description(
                ttv_dir, ttv_description
            )

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
