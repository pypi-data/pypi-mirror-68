# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from typing import TYPE_CHECKING, Any, Optional

import dependency_injector.providers as providers
from PySide2.QtCore import QAbstractListModel, QModelIndex, Qt

from dial_core.datasets.io import PredefinedTTVSetsContainer
from dial_core.utils import log

if TYPE_CHECKING:
    from PySide2.QtWidgets import QObject


LOGGER = log.get_logger(__name__)


class TTVSetsListModel(QAbstractListModel):
    def __init__(
        self, ttv_sets_list, parent: "QObject" = None,
    ):
        super().__init__(parent)

        self._ttv_sets_list = ttv_sets_list

        LOGGER.debug(
            "Initializing model with %d entries: %s",
            len(self._ttv_sets_list),
            self._ttv_sets_list,
        )

    def rowCount(self, parent=QModelIndex()) -> int:
        return len(self._ttv_sets_list)

    def index(self, row: int, column: int = 0, parent=QModelIndex()) -> "QModelIndex":
        return self.createIndex(row, column, self._ttv_sets_list[row])

    def data(self, index, role=Qt.DisplayRole) -> Optional[Any]:
        if role == Qt.DisplayRole:
            return str(self._ttv_sets_list[index.row()])

        return None

    def __reduce__(self):
        return (TTVSetsListModel, (self._ttv_sets_list,))


TTVSetsListModelFactory = providers.Factory(TTVSetsListModel)

PredefinedTTVSetsListModelFactory = providers.Factory(
    TTVSetsListModel,
    ttv_sets_list=[
        loader() for loader in PredefinedTTVSetsContainer.providers.values()
    ],
)
