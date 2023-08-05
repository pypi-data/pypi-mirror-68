# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from enum import Enum
from typing import Optional

import dependency_injector.providers as providers
from dial_core.datasets import Dataset, TTVSets  # noqa: F401
from PySide2.QtCore import QSize
from PySide2.QtWidgets import QLabel, QLineEdit, QVBoxLayout, QWidget


class TTVSetsMergerWidget(QWidget):
    class DatasetStatus(Enum):
        Valid = "#009211"
        Undefined = "#B6002A"

    def __init__(self, parent: "QWidget" = None):
        super().__init__(parent)

        # Components
        self._train: Optional["Dataset"] = None
        self._test: Optional["Test"] = None
        self._validation: Optional["Validation"] = None

        self._ttv: "TTVSets" = TTVSets(
            name="TTV Groups",
            train=self._train,
            test=self._test,
            validation=self._validation,
        )

        # Widgets
        self._name_lineedit = QLineEdit(self._ttv.name)
        self._train_label = QLabel("Train")
        self._test_label = QLabel("Test")
        self._validation_label = QLabel("Validation")

        self._train_status = self.DatasetStatus.Undefined
        self._test_status = self.DatasetStatus.Undefined
        self._validation_status = self.DatasetStatus.Undefined

        self._update_label_colors()

        self._main_layout = QVBoxLayout()
        self._main_layout.addWidget(self._name_lineedit)
        self._main_layout.addWidget(self._train_label)
        self._main_layout.addWidget(self._test_label)
        self._main_layout.addWidget(self._validation_label)

        self.setLayout(self._main_layout)

        # Connections
        self._name_lineedit.textChanged.connect(self.set_ttv_name)

    def set_ttv_name(self, name: str):
        """Sets a new name for the TTVSets object."""
        self._ttv.name = name

    def set_train(self, train: Optional["Dataset"]):
        """Sets a new Train Dataset to the TTVSets."""
        self._ttv.train = train

        self._update_dataset_statuses()
        self._update_label_colors()

    def set_test(self, test: Optional["Dataset"]):
        """Sets a new Test Dataset to the TTVSets."""
        self._ttv.test = test

        self._update_dataset_statuses()
        self._update_label_colors()

    def set_validation(self, validation: Optional["Dataset"]):
        """Sets a new Validation Dataset to the TTVSets."""
        self._ttv.validation = validation

        self._update_dataset_statuses()
        self._update_label_colors()

    def get_ttv(self) -> Optional["TTVSets"]:
        """Returns the generated TTVSets object."""
        return self._ttv

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
            self.DatasetStatus.Valid if self._ttv.test else self.DatasetStatus.Undefined
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


TTVSetsMergerWidgetFactory = providers.Factory(TTVSetsMergerWidget)
