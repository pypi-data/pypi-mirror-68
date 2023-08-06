# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

import re
from typing import Callable, List, Optional

import dependency_injector.providers as providers
from dial_core.utils import log
from PySide2.QtCore import QSize
from PySide2.QtWidgets import (
    QCheckBox,
    QComboBox,
    QFormLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QSizePolicy,
    QSpinBox,
    QWidget,
)
from tensorflow.keras.models import Model  # noqa: F401

from .predefined_models_window import PredefinedModelsWindowFactory

LOGGER = log.get_logger(__name__)


class PredefinedModelsWidget(QWidget):
    def __init__(self, predefined_models_window, parent: "QWidget" = None):
        super().__init__(parent)

        # Model picker size (left)
        self._predefined_models_window = predefined_models_window

        self._predefined_models_group = QGroupBox("Predefined Models:")
        self._predefined_models_layout = QHBoxLayout()
        self._predefined_models_layout.setContentsMargins(0, 0, 0, 0)
        self._predefined_models_group.setLayout(self._predefined_models_layout)
        self._predefined_models_layout.addWidget(self._predefined_models_window)

        # Description Side (right)
        self._model_name = QLabel("")

        self._include_top = QCheckBox("Include")
        self._include_top.setChecked(True)

        self._shape_textbox = QLineEdit("(224, 224, 3)")
        self._shape_textbox.setEnabled(False)

        self._classes_intbox = QSpinBox()
        self._classes_intbox.setMinimum(2)
        self._classes_intbox.setMaximum(999999)
        self._classes_intbox.setValue(1000)

        self._weights_combobox = QComboBox()
        self._weights_combobox.addItem("Imagenet", "imagenet")
        self._weights_combobox.addItem("None", None)

        # Add widgets to layout
        self._description_group = QGroupBox("Description:")
        self._description_layout = QFormLayout()

        self._description_group.setLayout(self._description_layout)

        self._description_layout.addRow("Name:", self._model_name)
        self._description_layout.addRow("Include Top:", self._include_top)
        self._description_layout.addRow("Input Shape:", self._shape_textbox)
        self._description_layout.addRow("Classes:", self._classes_intbox)
        self._description_layout.addRow("Weights:", self._weights_combobox)

        self._main_layout = QHBoxLayout()
        self._main_layout.addWidget(self._predefined_models_group)
        self._main_layout.addWidget(self._description_group)

        self.setLayout(self._main_layout)

        sp_left = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sp_left.setHorizontalStretch(1)

        self._predefined_models_group.setSizePolicy(sp_left)

        sp_right = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sp_right.setHorizontalStretch(2.5)

        self._description_group.setSizePolicy(sp_right)

        self._include_top.stateChanged.connect(lambda: self._update_enabled_widgets())
        self._weights_combobox.currentIndexChanged[int].connect(
            lambda: self._update_enabled_widgets()
        )

        self._predefined_models_window.selected_model_changed.connect(
            self._update_description_labels
        )

        self._update_enabled_widgets()

    def get_model(self) -> Optional["Model"]:
        try:
            LOGGER.debug("Include Top: %s", self._include_top.isChecked())
            LOGGER.debug("Classes: %s", self._classes_intbox.value())
            LOGGER.debug("Weights: %s", self._weights_combobox.currentData())

            if not self._include_top.isChecked():
                input_shape = tuple(
                    map(int, re.sub("[()]", "", self._shape_textbox.text()).split(","))
                )

                LOGGER.debug("Input tuple: %s", input_shape)

                return self._predefined_models_window.get_selected_model()["loader"](
                    include_top=False,
                    input_shape=input_shape,
                    weights=self._weights_combobox.currentData(),
                )

            return self._predefined_models_window.get_selected_model()["loader"](
                include_top=True,
                classes=self._classes_intbox.value(),
                weights=self._weights_combobox.currentData(),
            )

        except TypeError as err:
            LOGGER.exception(err)
            return None

    def get_image_transformations(self) -> List[Callable]:
        try:
            transformations = self._predefined_models_window.get_selected_model()[
                "transformations"
            ]

            return transformations

        except KeyError as err:
            LOGGER.exception(err)
            return None

    def _update_description_labels(self, model_desc: dict):
        self._model_name.setText(model_desc["name"])

    def _update_enabled_widgets(self):
        self._shape_textbox.setEnabled(not self._include_top.isChecked())

        if (
            self._include_top.isChecked()
            and self._weights_combobox.currentText() == "None"
        ):
            self._classes_intbox.setEnabled(True)
        else:
            self._classes_intbox.setEnabled(False)

    def sizeHint(self) -> "QSize":
        return QSize(400, 170)


PredefinedModelsWidgetFactory = providers.Factory(
    PredefinedModelsWidget, predefined_models_window=PredefinedModelsWindowFactory
)
