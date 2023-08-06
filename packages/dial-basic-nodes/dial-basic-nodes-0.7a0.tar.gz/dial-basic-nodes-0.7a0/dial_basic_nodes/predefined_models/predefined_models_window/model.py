# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from typing import TYPE_CHECKING, Any, Optional

import dependency_injector.providers as providers
from dial_core.utils import log
from PySide2.QtCore import QAbstractListModel, QModelIndex, Qt
from tensorflow.keras.applications import vgg16, vgg19

if TYPE_CHECKING:
    from PySide2.QtWidgets import QObject


LOGGER = log.get_logger(__name__)

PREDEFINED_MODELS_LIST = [
    {
        "name": "VGG16",
        "loader": vgg16.VGG16,
        "transformations": [vgg16.preprocess_input],
    },
    {
        "name": "VGG19",
        "loader": vgg19.VGG19,
        "transformations": [vgg19.preprocess_input],
    },
]


class PredefinedModelsModel(QAbstractListModel):
    def __init__(
        self, predefined_models_list, parent: "QObject" = None,
    ):
        super().__init__(parent)

        self._predefined_models_list = predefined_models_list

        LOGGER.debug(
            "Loaded %s predefined models: %s",
            len(self._predefined_models_list),
            self._predefined_models_list,
        )

    def rowCount(self, parent=QModelIndex()) -> int:
        return len(self._predefined_models_list)

    def index(self, row: int, column: int = 0, parent=QModelIndex()) -> "QModelIndex":
        return self.createIndex(row, column, self._predefined_models_list[row])

    def data(self, index, role=Qt.DisplayRole) -> Optional[Any]:
        if role == Qt.DisplayRole:
            return self._predefined_models_list[index.row()]["name"]

        return None

    def __reduce__(self):
        return (PredefinedModelsModel, (self._predefined_models_list,))


PredefinedModelsModelFactory = providers.Factory(
    PredefinedModelsModel, predefined_models_list=PREDEFINED_MODELS_LIST
)
