# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from typing import TYPE_CHECKING, List, Optional

from dial_core.utils import Dial
from PySide2.QtCore import (
    QByteArray,
    QDataStream,
    QIODevice,
    QMimeData,
    QModelIndex,
    Qt,
)
from tensorflow import keras

from .abstract_tree_model import AbstractTreeModel, AbstractTreeNode

if TYPE_CHECKING:
    from PySide2.QtWidgets import QWidget


class LayerNode(AbstractTreeNode):
    def __init__(
        self,
        display_name: str,
        layer: "keras.layers.Layer",
        layer_name: str = None,
        parent: "AbstractTreeNode" = None,
    ):
        super().__init__(
            [display_name, layer], parent,
        )

        # Set an specific name for the layer
        if layer_name:
            layer._name = layer_name

    @property
    def name(self) -> Optional[str]:
        return self.values[0]

    @property
    def layer(self) -> "keras.layers.Layer":
        return self.values[1]


class TitleNode(AbstractTreeNode):
    def __init__(self, name: str, parent: "AbstractTreeNode" = None):
        super().__init__([name], parent)

    @property
    def name(self) -> str:
        return self.values[0]


class LayersTreeModel(AbstractTreeModel):
    def __init__(self, parent: "QWidget" = None):
        super().__init__(parent)

        self.setup_model_data()

    def columnCount(self, parent=QModelIndex()) -> int:
        return 1

    def setup_model_data(self):
        core_layers = TitleNode("Core Layers")
        core_layers.append(
            LayerNode("Dense", keras.layers.Dense(10), layer_name="dense")
        )

        core_layers.append(
            LayerNode("Flatten", keras.layers.Flatten(), layer_name="flatten")
        )

        core_layers.append(
            LayerNode("Dropout", keras.layers.Dropout(0.5), layer_name="dropout")
        )

        activation_layers = TitleNode("Activation Layers")

        activation_layers.append(
            LayerNode("Linear", keras.layers.Activation("linear"), layer_name="linear")
        )
        activation_layers.append(
            LayerNode("ELU", keras.layers.Activation("elu"), layer_name="elu")
        )
        activation_layers.append(
            LayerNode("ReLU", keras.layers.Activation("relu"), layer_name="relu")
        )
        activation_layers.append(
            LayerNode(
                "Sigmoid", keras.layers.Activation("sigmoid"), layer_name="sigmoid"
            )
        )
        activation_layers.append(
            LayerNode(
                "Softmax", keras.layers.Activation("softmax"), layer_name="softmx"
            )
        )

        convolutional_layers = TitleNode("Convolutional Layers")
        convolutional_layers.append(
            LayerNode("Conv1D", keras.layers.Conv1D(32, 3), layer_name="conv1d")
        )
        convolutional_layers.append(
            LayerNode("Conv2D", keras.layers.Conv2D(32, 3), layer_name="conv2d")
        )
        convolutional_layers.append(
            LayerNode("Conv3D", keras.layers.Conv3D(32, 3), layer_name="conv3d")
        )

        pooling_layers = TitleNode("Pooling Layers")
        pooling_layers.append(
            LayerNode(
                "MaxPooling1D", keras.layers.MaxPooling1D(), layer_name="max_pool_1d"
            )
        )
        pooling_layers.append(
            LayerNode(
                "MaxPooling2D", keras.layers.MaxPooling2D(), layer_name="max_pool_2d"
            )
        )
        pooling_layers.append(
            LayerNode(
                "MaxPooling3D", keras.layers.MaxPooling3D(), layer_name="max_pool_3d"
            )
        )

        normalization_layers = TitleNode("Normalization Layers")
        normalization_layers.append(
            LayerNode(
                "BatchNormalization",
                keras.layers.BatchNormalization(),
                layer_name="batch_norm",
            )
        )
        normalization_layers.append(
            LayerNode(
                "LayerNormalization",
                keras.layers.LayerNormalization(),
                layer_name="layer_norm",
            )
        )

        self.root_node.append(core_layers)
        self.root_node.append(activation_layers)
        self.root_node.append(convolutional_layers)
        self.root_node.append(pooling_layers)
        self.root_node.append(normalization_layers)

    def headerData(
        self, section: int, orientation: "Qt.Orientation", role=Qt.DisplayRole
    ):
        """Returns the name of the headers."""

        if role != Qt.DisplayRole:
            return None

        # Column header must have their respective names
        if orientation == Qt.Horizontal:
            if section == 0:
                return "Layers"

        return None

    def flags(self, index: "QModelIndex"):
        """
        Flag items depending on its type.

        For example, only items of type LayerNode can be dragged.
        """
        if not index.isValid():
            return Qt.ItemIsEnabled

        general_flags = super().flags(index)

        if isinstance(index.internalPointer(), LayerNode):
            return general_flags | Qt.ItemIsDragEnabled

        return general_flags

    def mimeTypes(self) -> List[str]:
        """
        MIME Types supported by this model. In this case, the only supported MIME type
        is the one representing a list of Keras Layer.
        """
        return [Dial.KerasLayerListMIME.value]

    def mimeData(self, indexes: List["QModelIndex"]) -> "QMimeData":
        """
        Returns a serialized object representing a List of Keras Layer. Used for
        drag/drop operations, for example.
        """
        mime_data = QMimeData()

        # Serializer
        encoded_data = QByteArray()
        stream = QDataStream(encoded_data, QIODevice.WriteOnly)

        # Write all the layers corresponding to the indexes
        for index in indexes:
            if index.isValid():
                layer = index.internalPointer().layer
                stream.writeQVariant(layer)

        # Store the serialized data on the MIME data
        mime_data.setData(Dial.KerasLayerListMIME.value, encoded_data)

        return mime_data
