# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

import dependency_injector.providers as providers
from dial_core.datasets.datatype import DataTypeContainer
from PySide2.QtWidgets import QComboBox, QGroupBox, QStackedWidget, QVBoxLayout, QWidget

from .categorical_widget import CategoricalWidgetFactory

DATATYPE_TO_WIDGET = {DataTypeContainer.Categorical: CategoricalWidgetFactory}


class DatatypeSelector(QGroupBox):
    def __init__(self, title: str, datatype_to_widget, parent: "QWidget" = None):
        super().__init__(title, parent)

        # Maps a datatype with its respective widget. The widget is optional
        self._datatype_to_widget = datatype_to_widget

        self._datatype_combobox = QComboBox()

        self._stacked_widgets = QStackedWidget()

        for (i, (name, datatype_factory)) in enumerate(
            DataTypeContainer.providers.items()
        ):
            datatype_instance = datatype_factory()
            self._datatype_combobox.addItem(name, datatype_instance)

            if datatype_factory in self._datatype_to_widget:
                self._stacked_widgets.insertWidget(
                    i, self._datatype_to_widget[datatype_factory](datatype_instance)
                )

        self._main_layout = QVBoxLayout()
        self._main_layout.addWidget(self._datatype_combobox)
        self._main_layout.addWidget(self._stacked_widgets)

        self.setLayout(self._main_layout)

        self._datatype_combobox.currentIndexChanged[int].connect(
            self._change_active_widget
        )

    @property
    def selected_datatype(self):
        return self._datatype_combobox.currentData()

    def change_current_datatype(self, new_datatype_dict: dict):
        index = self._datatype_combobox.findText(new_datatype_dict["class"])

        if index != -1:
            self._datatype_combobox.setCurrentIndex(index)
            self._datatype_combobox.currentData().from_dict(new_datatype_dict)
            self._stacked_widgets.currentWidget().reload()

    def _change_active_widget(self, index):
        self._stacked_widgets.setCurrentIndex(index)

        # Hide the `stacked_widgets` when the current datatype doesn't needs to display
        # a widget
        if self._stacked_widgets.currentIndex() != index:
            self._stacked_widgets.setVisible(False)
        else:
            self._stacked_widgets.setVisible(True)

    def to_dict(self):
        return self.selected_datatype.to_dict()


DatatypeSelectorFactory = providers.Factory(
    DatatypeSelector, datatype_to_widget=DATATYPE_TO_WIDGET
)
