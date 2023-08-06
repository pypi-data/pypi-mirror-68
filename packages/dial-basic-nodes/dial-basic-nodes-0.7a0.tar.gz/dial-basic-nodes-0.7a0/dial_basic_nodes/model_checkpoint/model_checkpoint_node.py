# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from typing import TYPE_CHECKING, List

import dependency_injector.providers as providers
from dial_core.node_editor import Node
from tensorflow.keras.callbacks import Callback

from .model_checkpoint_widget import ModelCheckpointWidgetFactory

if TYPE_CHECKING:
    from .model_checkpoint_widget import ModelCheckpointWidget


class ModelCheckpointNode(Node):
    def __init__(
        self, model_checkpoint_widget: "ModelCheckpointWidget",
    ):
        super().__init__(
            title="Model Checkpoint", inner_widget=model_checkpoint_widget,
        )

        self.add_output_port("Keras Callbacks", port_type=List[Callback])
        self.outputs["Keras Callbacks"].set_generator_function(
            self.inner_widget.get_callbacks
        )

    def __reduce__(self):
        return (ModelCheckpointNode, (self.inner_widget,), super().__getstate__())


ModelCheckpointNodeFactory = providers.Factory(
    ModelCheckpointNode, model_checkpoint_widget=ModelCheckpointWidgetFactory,
)
