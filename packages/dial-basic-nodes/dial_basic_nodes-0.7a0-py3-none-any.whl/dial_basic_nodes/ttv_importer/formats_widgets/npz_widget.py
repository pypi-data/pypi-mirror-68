# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

import os

import dependency_injector.providers as providers
from dial_core.datasets import TTVSets
from dial_core.datasets.datatype import DataType
from dial_core.datasets.io import NpzDatasetIO
from dial_core.utils import log
from PySide2.QtWidgets import QVBoxLayout, QWidget

from .file_loader_group import FileLoaderGroup

LOGGER = log.get_logger(__name__)


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

        def load_dataset(filename):
            return (
                NpzDatasetIO()
                .set_x_type(x_type)
                .set_y_type(y_type)
                .set_filename(filename)
                .load(parent_dir="")  # Absolute path set on filename
            )

        train = load_dataset(self._train_file_loader.path)
        test = load_dataset(self._test_file_loader.path)
        validation = load_dataset(self._validation_file_loader.path)

        return TTVSets(name, train, test, validation)

    def update_widgets(self, ttv_dir: str, ttv_description: dict):
        def update_file_loader_path(file_loader, dataset_dir, dataset_description):
            if "filename" in dataset_description:
                file_loader.path = os.path.join(
                    ttv_dir, dataset_dir, dataset_description["filename"]
                )
            else:
                file_loader.path = ""

        update_file_loader_path(
            self._train_file_loader, "train", ttv_description["train"]
        )
        update_file_loader_path(self._test_file_loader, "test", ttv_description["test"])
        update_file_loader_path(
            self._validation_file_loader, "validation", ttv_description["validation"]
        )


NpzWidgetFactory = providers.Factory(NpzWidget)
