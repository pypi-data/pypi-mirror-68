# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from typing import Optional

import dependency_injector.providers as providers
from dial_core.datasets.io import TTVSetsLoader
from PySide2.QtCore import Signal
from PySide2.QtWidgets import QVBoxLayout, QWidget

from .ttv_sets_list import PredefinedTTVSetsListWidgetFactory


class PredefinedTTVSetsWidget(QWidget):
    selected_ttv_loader_changed = Signal(TTVSetsLoader)

    def __init__(self, predefined_ttv_sets_window, parent: "QWidget" = None):
        super().__init__(parent)

        self._predefined_ttv_sets_window = predefined_ttv_sets_window

        self._main_layout = QVBoxLayout()
        self._main_layout.setContentsMargins(0, 0, 0, 0)
        self._main_layout.addWidget(predefined_ttv_sets_window)

        self._predefined_ttv_sets_window.selected_ttv_loader_changed.connect(
            lambda ttv_loader: self.selected_ttv_loader_changed.emit(ttv_loader)
        )

        self.setLayout(self._main_layout)

    def get_ttv(self) -> Optional["TTVSets"]:
        return self._predefined_ttv_sets_window.selected_ttv()


PredefinedTTVSetsWidgetFactory = providers.Factory(
    PredefinedTTVSetsWidget,
    predefined_ttv_sets_window=PredefinedTTVSetsListWidgetFactory,
)
