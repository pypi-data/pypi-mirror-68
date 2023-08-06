# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from enum import Enum
from typing import Optional

import dependency_injector.providers as providers
from dial_core.datasets import Dataset, TTVSets  # noqa: F401
from PySide2.QtCore import QSize
from PySide2.QtWidgets import QLabel, QVBoxLayout, QWidget


class TTVSetsSplitterWidget(QWidget):
    class DatasetStatus(Enum):
        Valid = "#009211"
        Undefined = "#B6002A"

    def __init__(self, parent: "QWidget" = None):
        super().__init__(parent)

        # Components
        self._ttv: Optional["TTVSets"] = None

        # Widgets
        self._train_label = QLabel("Train")
        self._test_label = QLabel("Test")
        self._validation_label = QLabel("Validation")

        self._train_status = self.DatasetStatus.Undefined
        self._test_status = self.DatasetStatus.Undefined
        self._validation_status = self.DatasetStatus.Undefined

        self._update_label_colors()

        self._main_layout = QVBoxLayout()
        self._main_layout.addWidget(self._train_label)
        self._main_layout.addWidget(self._test_label)
        self._main_layout.addWidget(self._validation_label)

        self.setLayout(self._main_layout)

    def set_ttv(self, ttv: Optional["TTVSets"]):
        """Sets a new TTVSets to split."""
        self._ttv = ttv

        self._update_dataset_statuses()
        self._update_label_colors()

    def get_train(self) -> Optional["Dataset"]:
        """Returns the Train Dataset object of `_ttv`"""
        return self._ttv.train if self._ttv else None

    def get_test(self) -> Optional["Dataset"]:
        """Returns the Test Dataset object of `_ttv`"""
        return self._ttv.test if self._ttv else None

    def get_validation(self) -> Optional["Dataset"]:
        """Returns the Validation Dataset object of `_ttv`"""
        return self._ttv.validation if self._ttv else None

    def _update_dataset_statuses(self):
        if not self._ttv:
            self._train_status = self.DatasetStatus.Undefined
            self._test_status = self.DatasetStatus.Undefined
            self._validation_status = self.DatasetStatus.Undefined
            return

        self._train_status = (
            self.DatasetStatus.Valid
            if self._ttv.train
            else self.DatasetStatus.Undefined
        )

        self._test_status = (
            self.DatasetStatus.Valid
            if self._ttv.test
            else self.DatasetStatus.Undefined
        )

        self._validation_status = (
            self.DatasetStatus.Valid
            if self._ttv.validation
            else self.DatasetStatus.Undefined
        )

    def _update_label_colors(self):
        def set_label_color(label: "QLabel", color: str):
            label.setStyleSheet("QLabel {" + f"color: {color}" "}")

        set_label_color(self._train_label, self._train_status.value)
        set_label_color(self._test_label, self._test_status.value)
        set_label_color(self._validation_label, self._validation_status.value)

    def sizeHint(self) -> "QSize":
        """Returns the preferred size for this widget."""
        return QSize(200, 100)


TTVSetsSplitterWidgetFactory = providers.Factory(TTVSetsSplitterWidget)
