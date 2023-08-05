# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from typing import TYPE_CHECKING

import dependency_injector.providers as providers
from dial_core.datasets import Dataset
from dial_core.node_editor import Node
from tensorflow import keras

from .test_model_widget import TestModelWidgetFactory

if TYPE_CHECKING:
    from .test_model_widget import TestModelWidget


class TestModelNode(Node):
    def __init__(self, test_model_widget: "TestModelWidget"):
        super().__init__(title="Test Model", inner_widget=test_model_widget)

        self.add_input_port("Test Dataset", port_type=Dataset)
        self.add_input_port("Trained Model", port_type=keras.models.Model)

        self.inputs["Test Dataset"].set_processor_function(
            self.inner_widget.set_test_dataset
        )
        self.inputs["Trained Model"].set_processor_function(
            self.inner_widget.set_trained_model
        )

    def __reduce__(self):
        (TestModelNode, (self.inner_widget,), super().__getstate__())


TestModelNodeFactory = providers.Factory(
    TestModelNode, test_model_widget=TestModelWidgetFactory
)
