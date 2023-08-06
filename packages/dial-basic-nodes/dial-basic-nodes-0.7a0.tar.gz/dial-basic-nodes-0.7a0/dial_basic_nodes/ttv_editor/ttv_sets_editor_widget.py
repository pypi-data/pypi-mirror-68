# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from typing import Optional

import dependency_injector.providers as providers
from dial_core.datasets import TTVSets
from dial_core.utils import log
from PySide2.QtCore import QSize
from PySide2.QtWidgets import QFormLayout, QGridLayout, QLabel, QSplitter, QWidget

from .ttv_sets_tabs import TTVSetsTabs, TTVSetsTabsFactory

LOGGER = log.get_logger(__name__)


class TTVSetsEditorWidget(QWidget):
    """
    The TTVSetsEditorNodeWidget class provides a window for displaying all the
    information related to TTVSets
        * Tabs with the Train/Test/Validation data
        * Labels with information about the datasets length, data types, etc.
    """

    def __init__(self, ttv_tabs: "TTVSetsTabs", parent: "QWidget" = None):
        super().__init__(parent)

        # Components
        self._ttv: Optional["TTVSets"] = None

        # Initialize widgets
        self._main_layout = QGridLayout()
        self._ttv_info_layout = QFormLayout()

        self._ttv_tabs = ttv_tabs
        self._ttv_tabs.setParent(self)

        self._ttv_name_label = QLabel("")

        self._train_len_label = QLabel("0")
        self._test_len_label = QLabel("0")
        self._validation_len_label = QLabel("0")

        self._train_shape_label = QLabel("()")

        # Configure interface
        self._setup_ui()

    def get_ttv(self) -> Optional["TTVSets"]:
        """Returns the TTVSets object displayed by this widget."""
        return self._ttv

    def set_ttv(self, ttv: Optional["TTVSets"]):
        """Sets the TTVSets object to visualize."""
        self._ttv = ttv

        self._ttv_tabs.set_ttv(ttv)

        self._update_labels_text()

    def _update_labels_text(self):
        """
        Updates the text on each widget label to reflect the `_ttv` information.
        """
        LOGGER.info(f"Updating labels using {self._ttv}")

        name = self._ttv.name if self._ttv else ""

        def get_row_count_of(dataset):
            if not dataset:
                return 0

            return dataset.row_count()

        train_len = get_row_count_of(self._ttv.train) if self._ttv else 0
        test_len = get_row_count_of(self._ttv.test) if self._ttv else 0
        validation_len = get_row_count_of(self._ttv.validation) if self._ttv else 0

        self._ttv_name_label.setText(name)
        self._train_len_label.setText(str(train_len))
        self._test_len_label.setText(str(test_len))
        self._validation_len_label.setText(str(validation_len))

        print(">>> Update shape")
        self._train_shape_label.setText(
            f"X: {self._ttv.train.input_shape}. Y: {self._ttv.train.output_shape}"
            if self._ttv.train
            else "N/A"
        )

    def _setup_ui(self):
        """Widget layout configuration."""
        splitter = QSplitter()

        # Set label names
        self._ttv_info_layout.setFieldGrowthPolicy(QFormLayout.FieldsStayAtSizeHint)
        self._ttv_info_layout.addRow("Name ", self._ttv_name_label)
        self._ttv_info_layout.addRow("Total items (train)", self._train_len_label)
        self._ttv_info_layout.addRow("Total items (test)", self._test_len_label)
        self._ttv_info_layout.addRow(
            "Total items (validation)", self._validation_len_label
        )
        self._ttv_info_layout.addRow("Shape (train): ", self._train_shape_label)

        ttv_info_widget = QWidget()
        ttv_info_widget.setLayout(self._ttv_info_layout)

        splitter.addWidget(ttv_info_widget)
        splitter.addWidget(self._ttv_tabs)

        self._main_layout.addWidget(splitter, 0, 0)
        self._main_layout.setContentsMargins(0, 0, 0, 0)

        self.setLayout(self._main_layout)

    def sizeHint(self) -> "QSize":
        """Optimal size of the widget."""
        return QSize(500, 300)

    def __reduce__(self):
        return (TTVSetsEditorWidget, (self._ttv_tabs,))


TTVSetsEditorWidgetFactory = providers.Factory(
    TTVSetsEditorWidget, ttv_tabs=TTVSetsTabsFactory
)
