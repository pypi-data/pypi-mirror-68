# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

import os
from typing import Optional

import dependency_injector.providers as providers
from dial_core.datasets import TTVSets
from dial_core.datasets.io import TTVSetsIO
from dial_core.datasets.io.dataset_io import DatasetIORegistry
from dial_core.utils import log
from PySide2.QtWidgets import (
    QComboBox,
    QFileDialog,
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

LOGGER = log.get_logger(__name__)


class TTVSetsExporterWidget(QWidget):
    def __init__(
        self, dataset_io_providers=DatasetIORegistry, parent: "QWidget" = None,
    ):
        super().__init__(parent)

        # Components
        self._ttv: Optional["TTVSets"] = None
        self._dataset_io_providers = dataset_io_providers

        # Widgets
        self._name_textbox = QLineEdit("Unnamed TTV")
        self._name_textbox.setPlaceholderText("Name")

        self._train_label = QLabel("")
        self._test_label = QLabel("")
        self._validation_label = QLabel("")

        self._export_path_textbox = QLineEdit()
        self._export_path_textbox.setReadOnly(True)
        self._export_path_textbox.setPlaceholderText("Path...")
        self._export_path_button = QPushButton("Directory...")

        self._export_button = QPushButton("Export")
        self._export_button.clicked.connect(self.export_ttv)

        self._ttv_info_layout = QFormLayout()
        self._ttv_info_layout.addRow("Name:", self._name_textbox)
        self._ttv_info_layout.addRow("Train:", self._train_label)
        self._ttv_info_layout.addRow("Test:", self._test_label)
        self._ttv_info_layout.addRow("Validation:", self._validation_label)

        self._export_path_layout = QHBoxLayout()
        self._export_path_layout.addWidget(self._export_path_textbox)
        self._export_path_layout.addWidget(self._export_path_button)
        self._export_path_button.clicked.connect(self.pick_ttv_parent_dir)

        self._ttv_info_layout.addRow("Export Path:", self._export_path_layout)

        self._format_combobox = QComboBox()

        for (name, dataset_io_factory) in self._dataset_io_providers.providers.items():
            self._format_combobox.addItem(name, dataset_io_factory())

        self._ttv_info_layout.addRow("Format", self._format_combobox)

        self._main_layout = QVBoxLayout()
        self._main_layout.addLayout(self._ttv_info_layout)
        self._main_layout.addWidget(self._export_button)

        self.setLayout(self._main_layout)

    def set_ttv(self, ttv: "TTVSets"):
        """Sets a new TTVSets object for exporting."""
        self._ttv = ttv
        self._update_labels_text()

        LOGGER.info(f"TTVSets added to Export: {ttv}")

    def pick_ttv_parent_dir(self):
        LOGGER.debug("Picking a directory to export...")

        ttv_parent_dir = QFileDialog.getExistingDirectory(self, "Directory to export")

        self._export_path_textbox.setText(ttv_parent_dir)

        if ttv_parent_dir:
            LOGGER.info("%s selected", ttv_parent_dir)
        else:
            LOGGER.debug("Selection cancelled.")

    def export_ttv(self):
        if not self._export_path_textbox.text():
            LOGGER.info("TTV export parent directory not set!")
            return

        if not self._ttv:
            LOGGER.info("TTV not set!")
            return

        self._ttv.name = self._name_textbox.text()

        ttv_dir = self._export_path_textbox.text()
        description_file_path = os.path.join(ttv_dir, "ttv_description.json")

        dataset_io = self._format_combobox.currentData()
        LOGGER.debug("Using %s formatter...", dataset_io)

        ttv_description = TTVSetsIO.save_to_file(
            description_file_path, dataset_io, self._ttv
        )

        LOGGER.info("TTV Exported to %s", description_file_path)
        LOGGER.debug(ttv_description)

    def _update_labels_text(self):
        """Update the text labels to reflect the TTVSets information"""
        self._name_textbox.setText(self._ttv.name)
        self._train_label.setText(f"{str(self._ttv.train if self._ttv else None)}")
        self._test_label.setText(f"{str(self._ttv.test if self._ttv else None)}")
        self._validation_label.setText(
            f"{str(self._ttv.validation if self._ttv else None)}"
        )


TTVSetsExporterWidgetFactory = providers.Factory(TTVSetsExporterWidget)
