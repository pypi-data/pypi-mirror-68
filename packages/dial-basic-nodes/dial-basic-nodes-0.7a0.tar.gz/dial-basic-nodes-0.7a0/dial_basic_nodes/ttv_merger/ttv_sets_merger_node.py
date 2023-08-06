# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

import dependency_injector.providers as providers
from dial_core.datasets import Dataset, TTVSets
from dial_core.node_editor import Node

from .ttv_sets_merger_widget import TTVSetsMergerWidget, TTVSetsMergerWidgetFactory


class TTVSetsMergerNode(Node):
    """The TTVSetsMergerNode class provides a node for separating a TTVSets object
    into the individual Train/Test/Validation Datasets."""

    def __init__(self, ttv_sets_merger: "TTVSetsMergerWidget"):
        super().__init__(title="TTV Merger", inner_widget=ttv_sets_merger)

        self.add_input_port(name="Train Dataset", port_type=Dataset)
        self.add_input_port(name="Test Dataset", port_type=Dataset)
        self.add_input_port(name="Validation Dataset", port_type=Dataset)

        self.add_output_port(name="TTV Sets", port_type=TTVSets)

        self.inputs["Train Dataset"].set_processor_function(self._train_received)
        self.inputs["Test Dataset"].set_processor_function(self._test_received)
        self.inputs["Validation Dataset"].set_processor_function(
            self._validation_received
        )

        self.outputs["TTV Sets"].set_generator_function(self.inner_widget.get_ttv)

    def _train_received(self, train: "Dataset"):
        self.inner_widget.set_train(train)

        self.outputs["TTV Sets"].send()

    def _test_received(self, test: "Dataset"):
        self.inner_widget.set_test(test)

        self.outputs["TTV Sets"].send()

    def _validation_received(self, validation: "Dataset"):
        self.inner_widget.set_validation(validation)

        self.outputs["TTV Sets"].send()

    def __reduce__(self):
        return (TTVSetsMergerNode, (self.inner_widget,), super().__getstate__())


TTVSetsMergerNodeFactory = providers.Factory(
    TTVSetsMergerNode, ttv_sets_merger=TTVSetsMergerWidgetFactory
)
