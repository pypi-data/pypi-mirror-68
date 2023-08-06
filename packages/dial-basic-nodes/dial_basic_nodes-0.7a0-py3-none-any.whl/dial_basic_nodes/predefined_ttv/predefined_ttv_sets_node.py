# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:


from typing import TYPE_CHECKING

import dependency_injector.providers as providers
from dial_core.datasets import TTVSets
from dial_core.node_editor import Node

from .predefined_ttv_sets_widget import PredefinedTTVSetsWidgetFactory

if TYPE_CHECKING:
    from .predefined_ttv_sets_widget import PredefinedTTVSetsWidget


class PredefinedTTVSetsNode(Node):
    def __init__(self, predefined_ttv_sets_widget: "PredefinedTTVSetsWidget"):
        super().__init__(
            title="Predefined TTVSets Node", inner_widget=predefined_ttv_sets_widget
        )

        self.add_output_port(name="TTVSets", port_type=TTVSets)
        self.outputs["TTVSets"].set_generator_function(self.inner_widget.get_ttv)

        self.inner_widget.selected_ttv_loader_changed.connect(
            lambda: self.outputs["TTVSets"].send()
        )

    def __reduce__(self):
        return (PredefinedTTVSetsNode, (self.inner_widget,), super().__getstate__())


PredefinedTTVSetsNodeFactory = providers.Factory(
    PredefinedTTVSetsNode, predefined_ttv_sets_widget=PredefinedTTVSetsWidgetFactory
)
