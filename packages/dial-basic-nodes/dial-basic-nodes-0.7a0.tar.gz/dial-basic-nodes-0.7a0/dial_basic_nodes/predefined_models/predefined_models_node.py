# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from typing import TYPE_CHECKING, Callable, List

import dependency_injector.providers as providers
from dial_core.node_editor import Node
from tensorflow.keras.models import Model

from .predefined_models_widget import PredefinedModelsWidgetFactory

if TYPE_CHECKING:
    from .predefined_models_widget import PredefinedModelsWidget


class PredefinedModelsNode(Node):
    def __init__(self, predefined_models_widget: "PredefinedModelsWidget"):
        super().__init__(
            title="Predefined Models Node", inner_widget=predefined_models_widget
        )

        self.add_output_port(name="Image Transformations", port_type=List[Callable])
        self.add_output_port(name="Model", port_type=Model)

        self.outputs["Model"].set_generator_function(self.inner_widget.get_model)
        self.outputs["Image Transformations"].set_generator_function(
            self.inner_widget.get_image_transformations
        )

    def __reduce__(self):
        return (PredefinedModelsNode, (self.inner_widget,), super().__getstate__())


PredefinedModelsNodeFactory = providers.Factory(
    PredefinedModelsNode, predefined_models_widget=PredefinedModelsWidgetFactory
)
