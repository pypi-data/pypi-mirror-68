# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

import dependency_injector.providers as providers
from PySide2.QtWidgets import QLabel, QVBoxLayout, QWidget


class CategoricalImagesWidget(QWidget):
    def __init__(self, parent: "QWidget" = None):
        super().__init__(parent)

        self._main_layout = QVBoxLayout()
        self._main_layout.addWidget(QLabel("Not Implemented"))

        self.setLayout(self._main_layout)


CategoricalImagesWidgetFactory = providers.Factory(CategoricalImagesWidget)
