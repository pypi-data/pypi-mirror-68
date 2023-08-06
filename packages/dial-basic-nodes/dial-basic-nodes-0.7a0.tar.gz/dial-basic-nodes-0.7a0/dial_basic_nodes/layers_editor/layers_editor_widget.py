# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from typing import TYPE_CHECKING

import dependency_injector.providers as providers
from PySide2.QtCore import QSize, Signal
from PySide2.QtWidgets import QHBoxLayout, QSizePolicy, QWidget
from tensorflow.keras.models import Sequential

from .layers_tree import LayersTreeWidgetFactory
from .model_table import ModelTableWidgetFactory

if TYPE_CHECKING:
    from .layers_tree import LayersTreeWidget
    from .model_table import ModelTableWidget


class LayersEditorWidget(QWidget):
    """
    Window for all the model related operations (Create/Modify NN architectures)
    """

    layers_modified = Signal()

    def __init__(
        self,
        layers_tree: "LayersTreeWidget",
        model_table: "ModelTableWidget",
        parent: "QWidget" = None,
    ):
        super().__init__(parent)

        # Initialize Widgets
        self._layers_tree = layers_tree
        self._layers_tree.setParent(self)

        self._model_table = model_table
        self._model_table.setParent(self)

        # Configure Layout
        self._main_layout = QHBoxLayout()
        self._main_layout.setContentsMargins(0, 0, 0, 0)
        self._main_layout.addWidget(self._layers_tree)
        self._main_layout.addWidget(self._model_table)

        sp_left = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sp_left.setHorizontalStretch(1.3)

        self._layers_tree.setSizePolicy(sp_left)

        sp_mid = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sp_mid.setHorizontalStretch(3)

        self._model_table.setSizePolicy(sp_mid)

        self.setLayout(self._main_layout)

        # Setup connections
        self._model_table.layers_modified.connect(lambda: self.layers_modified.emit())

    def set_input_model(self, model):
        self._model_table.set_layers(model.layers)

    def get_output_model(self):
        model = Sequential()

        for layer in self._model_table.layers:
            model.add(layer)

        return model

    def sizeHint(self) -> "QSize":
        return QSize(600, 300)

    def __reduce__(self):
        return (LayersEditorWidget, (self._layers_tree, self._model_table))


LayersEditorWidgetFactory = providers.Factory(
    LayersEditorWidget,
    layers_tree=LayersTreeWidgetFactory,
    model_table=ModelTableWidgetFactory,
)
