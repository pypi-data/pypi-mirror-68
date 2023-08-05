# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from typing import TYPE_CHECKING, Optional

import dependency_injector.providers as providers
from PySide2.QtWidgets import QTabWidget

from dial_basic_nodes.utils.dataset_table import DatasetTableWidgetFactory

if TYPE_CHECKING:
    from PySide2.QtWidgets import QWidget


class TTVSetsTabs(QTabWidget):
    """
    The TTVSetsTabs class is a container for a pair of train/test datasets. Each
    dataset is displayed on its own tab, and can be accessed through the `train_dataset`
    and `test_dataset` methods.
    """

    def __init__(
        self,
        dataset_table_widget_factory: "providers.Factory",
        parent: "QWidget" = None,
    ):
        super().__init__(parent)

        # Dataset Tables
        self._train_table_widget = dataset_table_widget_factory(parent=self)
        self._test_table_widget = dataset_table_widget_factory(parent=self)
        self._validation_table_widget = dataset_table_widget_factory(parent=self)

        self.addTab(self._train_table_widget, "Train")
        self.addTab(self._test_table_widget, "Test")
        self.addTab(self._validation_table_widget, "Validation")

        # Factory for generating dataset tables (Used for recreating the widget on load)
        self._dataset_table_widget_factory = dataset_table_widget_factory

    def set_ttv(self, ttv: Optional["TTVSets"]):
        """Sets the TTVSets object to visualize."""
        train = ttv.train if ttv else None
        test = ttv.test if ttv else None
        validation = ttv.validation if ttv else None

        self._train_table_widget.load_dataset(train)
        self._test_table_widget.load_dataset(test)
        self._validation_table_widget.load_dataset(validation)

    def __reduce__(self):
        return (
            TTVSetsTabs,
            (self._dataset_table_widget_factory,),
        )


TTVSetsTabsFactory = providers.Factory(
    TTVSetsTabs, dataset_table_widget_factory=DatasetTableWidgetFactory.delegate()
)
