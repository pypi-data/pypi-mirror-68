# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from typing import List

import dependency_injector.providers as providers
from dial_core.utils import log
from PySide2.QtCore import QSize
from PySide2.QtWidgets import (
    QCheckBox,
    QFileDialog,
    QFormLayout,
    QGroupBox,
    QHBoxLayout,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
)
from tensorflow.keras.callbacks import Callback

LOGGER = log.get_logger(__name__)


class ModelCheckpointWidget(QWidget):
    def __init__(self, parent: "QWidget" = None):
        super().__init__(parent)

        # Widgets
        self._save_path_textbox = QLineEdit()
        self._save_path_textbox.setPlaceholderText("Directory to save model files...")
        self._save_path_button = QPushButton("Select...")
        self._save_path_button.clicked.connect(self._pick_save_directory)
        self._save_path_layout = QHBoxLayout()
        self._save_path_layout.addWidget(self._save_path_textbox)
        self._save_path_layout.addWidget(self._save_path_button)

        self._filename_textbox = QLineEdit("model.{epoch:02d}--{val_loss:.2f}.h5")

        self._weights_only_checkbox = QCheckBox("Weights only")

        # Layouts
        self._settings_layout = QFormLayout()
        self._settings_layout.addRow("Save directory:", self._save_path_layout)
        self._settings_layout.addRow("File name:", self._filename_textbox)
        self._settings_layout.addRow("Save weights only?", self._weights_only_checkbox)

        self._settings_group = QGroupBox("Model Checkpoint export settings")
        self._settings_group.setLayout(self._settings_layout)

        self._main_layout = QVBoxLayout()
        self._main_layout.addWidget(self._settings_group)

        self.setLayout(self._main_layout)

    def get_callbacks(self) -> List[Callback]:
        return []

    def _pick_save_directory(self):
        save_dir = QFileDialog.getExistingDirectory(self, "Save directory...")

        if save_dir:
            self._save_path_textbox.setText(save_dir)
        else:
            LOGGER.debug("Picking save directory cancelled.")

    def sizeHint(self) -> "QSize":
        return QSize(500, 200)

    def __reduce__(self):
        return (ModelCheckpointWidget, (), super().__getstate__())


ModelCheckpointWidgetFactory = providers.Factory(ModelCheckpointWidget)
