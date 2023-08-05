# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

import os

import dependency_injector.providers as providers
from dial_core.datasets import TTVSets
from dial_core.datasets.datatype import DataType
from dial_core.datasets.io import NpzDatasetIOBuilder, TTVSetsIO
from dial_core.utils import log
from PySide2.QtWidgets import (
    QFileDialog,
    QGroupBox,
    QHBoxLayout,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

LOGGER = log.get_logger(__name__)


class FileLoaderGroup(QGroupBox):
    def __init__(
        self,
        title: str,
        parent: "QWidget" = None,
        filter: str = "",
        pick_directories: bool = False,
    ):
        super().__init__(title, parent)

        self._file_picker_dialog = QFileDialog(
            caption=f'Picking a "{title}" file...', filter=filter
        )
        self._file_picker_dialog.setFileMode(
            QFileDialog.DirectoryOnly if pick_directories else QFileDialog.ExistingFile
        )

        self._pick_file_text = QLineEdit()
        self._pick_file_text.setReadOnly(True)
        self._pick_file_text.setPlaceholderText("Path...")
        self._pick_file_button = QPushButton("Load")

        self._pick_file_layout = QHBoxLayout()
        self._pick_file_layout.addWidget(self._pick_file_text)
        self._pick_file_layout.addWidget(self._pick_file_button)

        self._main_layout = QVBoxLayout()
        self._main_layout.addLayout(self._pick_file_layout)

        self.setLayout(self._main_layout)

        self._pick_file_button.clicked.connect(self._load_from_filesystem)

    @property
    def layout(self) -> "QVBoxLayout":
        return self._main_layout

    @property
    def path(self) -> str:
        return self._pick_file_text.text()

    @path.setter
    def path(self, path: str):
        self._pick_file_text.setText(path)

    def _load_from_filesystem(self):
        LOGGER.debug("Picking file...")

        if self._file_picker_dialog.exec():
            self._pick_file_text.setText(self._file_picker_dialog.selectedFiles()[0])


class NpzWidget(QWidget):
    def __init__(self, parent: "QWidget" = None):
        super().__init__(parent)

        self._train_file_loader = FileLoaderGroup("Train", filter="*.npz")
        self._test_file_loader = FileLoaderGroup("Test", filter="*.npz")
        self._validation_file_loader = FileLoaderGroup("Validation", filter="*.npz")

        self._main_layout = QVBoxLayout()
        self._main_layout.setContentsMargins(0, 0, 0, 0)
        self._main_layout.addWidget(self._train_file_loader)
        self._main_layout.addWidget(self._test_file_loader)
        self._main_layout.addWidget(self._validation_file_loader)

        self.setLayout(self._main_layout)

    def load_ttv(self, name: str, x_type: DataType, y_type: DataType):
        LOGGER.debug("Loading TTV %s", name)

        train = self._load_dataset(
            "train", self._train_file_loader.path, x_type, y_type
        )
        test = self._load_dataset("test", self._test_file_loader.path, x_type, y_type)
        validation = self._load_dataset(
            "validation", self._validation_file_loader.path, x_type, y_type
        )

        return TTVSets(name, train, test, validation)

    def load_ttv_from_description(self, ttv_dir: str, ttv_description):
        try:
            self._train_file_loader.path = os.path.join(
                ttv_dir, "train", ttv_description["train"]["filename"]
            )
        except KeyError:
            pass

        try:
            self._test_file_loader.path = os.path.join(
                ttv_dir, "test", ttv_description["test"]["filename"]
            )
        except KeyError:
            pass

        try:
            self._validation_file_loader.path = os.path.join(
                ttv_dir, "validation", ttv_description["validation"]["filename"]
            )
        except KeyError:
            pass

        return TTVSetsIO.load_ttv_from_description(ttv_dir, ttv_description)

    def _load_dataset(
        self, dataset_dir: str, filename_path: str, x_type: DataType, y_type: DataType
    ):
        return (
            NpzDatasetIOBuilder()
            .set_x_type(x_type)
            .set_y_type(y_type)
            .set_filename(filename_path)
            .load("")
        )


NpzWidgetFactory = providers.Factory(NpzWidget)
