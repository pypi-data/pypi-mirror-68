# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from typing import TYPE_CHECKING

import dependency_injector.providers as providers
from dial_core.datasets import TTVSets
from dial_core.node_editor import Node
from dial_core.utils import log

from .ttv_sets_editor_widget import TTVSetsEditorWidgetFactory

if TYPE_CHECKING:
    from .ttv_sets_editor_widget import TTVSetsEditorWidget

LOGGER = log.get_logger(__name__)


class TTVSetsEditorNode(Node):
    """The TTVSetsEditor class provides a node capable of load, visualize and modify
        Dataset objects through an interface."""

    def __init__(self, ttv_editor_widget: "TTVSetsEditorWidget"):
        super().__init__(title="Dataset Editor Node", inner_widget=ttv_editor_widget)

        self.add_input_port(name="TTV Sets", port_type=TTVSets)

        self.add_output_port(name="TTV Sets", port_type=TTVSets)

        self.inputs["TTV Sets"].set_processor_function(self._ttv_received)
        self.outputs["TTV Sets"].set_generator_function(self.inner_widget.get_ttv)

    def _ttv_received(self, ttv_sets: "TTVSets"):
        LOGGER.debug("TTV Received on {self}")

        self.inner_widget.set_ttv(ttv_sets)

        self.outputs["TTV Sets"].send()

    def __reduce__(self):
        return (TTVSetsEditorNode, (self.inner_widget,), super().__getstate__())


TTVSetsEditorNodeFactory = providers.Factory(
    TTVSetsEditorNode, ttv_editor_widget=TTVSetsEditorWidgetFactory
)
