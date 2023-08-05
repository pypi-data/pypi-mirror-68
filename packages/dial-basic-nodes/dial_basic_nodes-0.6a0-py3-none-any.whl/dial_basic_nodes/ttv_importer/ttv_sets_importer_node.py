# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from typing import TYPE_CHECKING

import dependency_injector.providers as providers
from dial_core.datasets import TTVSets
from dial_core.node_editor import Node
from dial_core.utils import log

from .ttv_sets_importer_widget import TTVSetsImporterWidgetFactory

if TYPE_CHECKING:
    from .ttv_sets_importer_widget import TTVSetsImporterWidget

LOGGER = log.get_logger(__name__)


class TTVSetsImporterNode(Node):
    """The TTVSetsImporterNode class provides several methods for loading datasets (from
    the file system or predefined datasets)"""

    def __init__(self, ttv_importer_widget: "TTVSetsImporterWidget", parent=None):
        super().__init__(
            title="TTV Importer Node", inner_widget=ttv_importer_widget, parent=parent
        )

        self.add_output_port(name="TTV Sets", port_type=TTVSets)
        self.outputs["TTV Sets"].set_generator_function(self.inner_widget.get_ttv)

        self.inner_widget.ttv_updated.connect(lambda: self.outputs["TTV Sets"].send())

    def __reduce__(self):
        return (TTVSetsImporterNode, (self.inner_widget,), super().__getstate__())


TTVSetsImporterNodeFactory = providers.Factory(
    TTVSetsImporterNode, ttv_importer_widget=TTVSetsImporterWidgetFactory
)
