# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

import dependency_injector.providers as providers
from dial_core.datasets import Dataset, TTVSets
from dial_core.node_editor import Node

from .ttv_sets_splitter_widget import (
    TTVSetsSplitterWidget,
    TTVSetsSplitterWidgetFactory,
)


class TTVSetsSplitterNode(Node):
    """The TTVSetsSplitterNode class provides a node for separating a TTVSets object
    into the individual Train/Test/Validation Datasets."""

    def __init__(self, ttv_sets_splitter: "TTVSetsSplitterWidget"):
        super().__init__(title="TTV Splitter", inner_widget=ttv_sets_splitter)

        self.add_input_port(name="TTV Sets", port_type=TTVSets)

        self.add_output_port(name="Train Dataset", port_type=Dataset)
        self.add_output_port(name="Test Dataset", port_type=Dataset)
        self.add_output_port(name="Validation Dataset", port_type=Dataset)

        self.inputs["TTV Sets"].set_processor_function(self._ttv_received)

        self.outputs["Train Dataset"].set_generator_function(
            self.inner_widget.get_train
        )
        self.outputs["Test Dataset"].set_generator_function(self.inner_widget.get_test)
        self.outputs["Validation Dataset"].set_generator_function(
            self.inner_widget.get_validation
        )

    def _ttv_received(self, ttv: "TTVSets"):
        self.inner_widget.set_ttv(ttv)

        self.outputs["Train Dataset"].send()
        self.outputs["Test Dataset"].send()
        self.outputs["Validation Dataset"].send()

    def __reduce__(self):
        return (TTVSetsSplitterNode, (self.inner_widget,), super().__getstate__())


TTVSetsSplitterNodeFactory = providers.Factory(
    TTVSetsSplitterNode, ttv_sets_splitter=TTVSetsSplitterWidgetFactory
)
