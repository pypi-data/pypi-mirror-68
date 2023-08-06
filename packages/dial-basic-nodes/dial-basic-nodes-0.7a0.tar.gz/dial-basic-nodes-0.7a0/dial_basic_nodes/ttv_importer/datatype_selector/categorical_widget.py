# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

import dependency_injector.providers as providers
from PySide2.QtWidgets import QLabel, QPlainTextEdit, QVBoxLayout, QWidget


class CategoricalWidget(QWidget):
    def __init__(self, categorical_datatype, parent: "QWidget" = None):
        super().__init__(parent)

        self._main_layout = QVBoxLayout()

        # Components
        self._categorical_datatype = categorical_datatype

        # Widgets
        self._categories_textarea = QPlainTextEdit()

        self._main_layout.addWidget(self._categories_textarea)
        self._main_layout.addWidget(QLabel("One category per row"))

        self.reload()

        self._categories_textarea.textChanged.connect(self.update_categories_list)

        self.setLayout(self._main_layout)

    def update_categories_list(self):
        categories = list(
            filter(
                lambda category: len(category) != 0,
                self._categories_textarea.toPlainText().split("\n"),
            )
        )
        self._categorical_datatype.categories = categories

        print(categories)

    def reload(self):
        self._categories_textarea.setPlainText(
            "\n".join(self._categorical_datatype.categories)
        )


CategoricalWidgetFactory = providers.Factory(CategoricalWidget)
