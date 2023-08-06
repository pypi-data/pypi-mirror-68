# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

import dependency_injector.providers as providers

from dial_core.node_editor import Node
from dial_core.datasets import TTVSets

from .ttv_sets_exporter_widget import (
    TTVSetsExporterWidget,
    TTVSetsExporterWidgetFactory,
)


class TTVSetsExporterNode(Node):
    """The TTVSetsExporterNode class provides several methods for saving datasets
    onto the file system."""

    def __init__(self, ttv_exporter_widget: "TTVSetsExporterWidget", parent=None):
        super().__init__(
            title="TTV Exporter Node", inner_widget=ttv_exporter_widget, parent=parent
        )

        self.add_input_port(name="TTV Sets", port_type=TTVSets)
        self.inputs["TTV Sets"].set_processor_function(self.inner_widget.set_ttv)

    def __reduce__(self):
        return (TTVSetsExporterNode, (self.inner_widget,), super().__getstate__())


TTVSetsExporterNodeFactory = providers.Factory(
    TTVSetsExporterNode, ttv_exporter_widget=TTVSetsExporterWidgetFactory
)
