# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from typing import Optional

import dependency_injector.providers as providers
from PySide2.QtWidgets import QVBoxLayout, QWidget
from tensorflow.keras.models import Model  # noqa: F401

from .predefined_models_window import PredefinedModelsWindowFactory


class PredefinedModelsWidget(QWidget):
    def __init__(self, predefined_models_window, parent: "QWidget" = None):
        super().__init__(parent)

        self._predefined_models_window = predefined_models_window

        self._main_layout = QVBoxLayout()
        self._main_layout.setContentsMargins(0, 0, 0, 0)
        self._main_layout.addWidget(predefined_models_window)

        self.setLayout(self._main_layout)

    def get_model(self) -> Optional["Model"]:
        return self._predefined_models_window.selected_model()


PredefinedModelsWidgetFactory = providers.Factory(
    PredefinedModelsWidget, predefined_models_window=PredefinedModelsWindowFactory
)
