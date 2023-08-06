# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from enum import IntEnum
from typing import TYPE_CHECKING, Any, Dict, List, Optional

import dependency_injector.providers as providers
from dial_core.datasets import Dataset
from dial_core.datasets.datatype import DataType
from dial_core.utils import log
from PySide2.QtCore import QAbstractTableModel, QModelIndex, Qt, Signal
from PySide2.QtGui import QPixmapCache

if TYPE_CHECKING:
    from PySide2.QtWidgets import QObject


LOGGER = log.get_logger(__name__)


class DatasetTableModel(QAbstractTableModel):
    TypeRole = Qt.UserRole + 1

    dataset_loaded = Signal(Dataset)

    class ColumnLabel(IntEnum):
        Input = 0
        Output = 1

    def __init__(self, parent: "QObject" = None):
        super().__init__(parent)

        self.max_row_batch_to_load = 100

        self._dataset: "Dataset" = Dataset()

        self._types: List[Optional[DataType]] = [
            self._dataset.x_type,
            self._dataset.y_type,
        ]
        self._loaded_types: List[Dict[str, DataType]] = [
            {type(self._dataset.x_type).__name__: self._dataset.x_type},
            {type(self._dataset.y_type).__name__: self._dataset.y_type},
        ]

        self._cached_data: List[List[Any]] = [[], []]

        self._role_map = {
            Qt.DisplayRole: self._display_role,
            self.TypeRole: self._type_role,
        }

    @property
    def dataset(self) -> "Dataset":
        """Returns the Dataset object this model is displaying."""
        return self._dataset

    def load_dataset(self, dataset: "Dataset"):
        """Loads a new dataset and starts fetching it on the model."""
        LOGGER.debug("Loading dataset %s...", dataset)

        self.clear()

        self._dataset = dataset

        if not dataset:
            return

        # Clear the loaded types
        self._types = [dataset.x_type, dataset.y_type]
        self._loaded_types = [
            {type(dataset.x_type).__name__: dataset.x_type},
            {type(dataset.y_type).__name__: dataset.y_type},
        ]

        self.dataset_loaded.emit(self._dataset)

    def clear(self):
        QPixmapCache.clear()
        self._cached_data.clear()
        self._cached_data = [[], []]

        self.modelReset.emit()

    def rowCount(self, parent=QModelIndex()) -> int:
        """Returns the number of rows on the dataset."""
        return len(self._data_of(self.ColumnLabel.Input))

    def columnCount(self, parent=QModelIndex()) -> int:
        """Returns the nubmer of columns on the dataset."""
        return len(self.ColumnLabel)

    def headerData(
        self, section: int, orientation: "Qt.Orientation", role=Qt.DisplayRole
    ):
        """Returns the name of the headers."""

        if role != Qt.DisplayRole:
            return None

        # Column header must have their respective names
        if orientation == Qt.Horizontal:
            return (
                f"{self.ColumnLabel(section).name} "
                f"({type(self._type_of(section)).__name__})"
            )

        # Row header will have the row number as name
        if orientation == Qt.Vertical:
            return str(section)

        return None

    def canFetchMore(self, parent: "QModelIndex") -> bool:
        """Checks if the model can fetch more data from the Dataset object."""
        if parent.isValid():
            return False

        if not self._dataset:
            return False

        return self.rowCount() < self._dataset.row_count()

    def fetchMore(self, parent: "QModelIndex") -> bool:
        """Loads more data from the Dataset object to the `self.__cached_data`
        variable.

        Returns if the fetch operation was sucessfully performed.
        """
        if parent.isValid() or not self._dataset:
            return False

        remainder = self._dataset.row_count() - self.rowCount()
        items_to_fetch = min(remainder, self.max_row_batch_to_load)

        if items_to_fetch <= 0:
            return False

        # Load new rows to the cached array
        row = self.rowCount()
        count = items_to_fetch

        return self.insertRows(row, row + count - 1, QModelIndex())

    def index(self, row: int, column: int, parent=QModelIndex()):
        """Creates an index for each row/column cell.

        Column 0 is X, column 1 is Y.
        """
        if row < 0 or row > self.rowCount():
            return QModelIndex()

        try:
            return self.createIndex(row, column, self._data_of(column)[row])
        except IndexError:
            return QModelIndex()

    def data(self, index: "QModelIndex", role=Qt.DisplayRole):
        """Returns the corresponding data depending on the specified role."""
        if not index.isValid():
            return None

        try:
            return self._role_map[role](index.row(), index.column())
        except KeyError:
            return None

    def insertRows(self, row: int, count: int, parent=QModelIndex()) -> bool:
        """Inserts new rows onto the model from the Dataset object.

        Important:
            This model DOES NOT add new rows to the inner Dataset object. For adding new
            rows, see the `insert_data` method.

        Returns:
            If the rows were inserted sucessfully.
        """
        if not self._dataset:
            return False

        self.beginInsertRows(QModelIndex(), row, row + count - 1)

        x_set, y_set = self._dataset.items(
            start=row, end=row + count, role=Dataset.Role.Display
        )

        self._data_of(self.ColumnLabel.Input)[row:row] = x_set
        self._data_of(self.ColumnLabel.Output)[row:row] = y_set

        self.endInsertRows()

        return True

    def removeRows(self, row: int, count: int, index=QModelIndex()) -> bool:
        """Removes rows from the model.

        Important:
            This model DOES NOT removes any rows from the inner Dataset object. For
            removing rows, see the `remove_data` method.

        Returns:
            If the rows were removed sucessfully.
        """
        if row < 0:
            return False

        LOGGER.debug("Remove rows BEGIN: row %s, %s items", row, count)
        LOGGER.debug("Previous model size: %s", self.rowCount())

        self.beginRemoveRows(QModelIndex(), row, row + count - 1)

        del self._data_of(self.ColumnLabel.Input)[row : row + count]
        del self._data_of(self.ColumnLabel.Output)[row : row + count]

        self.endRemoveRows()
        LOGGER.debug("Remove rows END")
        LOGGER.debug("New model size: %s", self.rowCount())

        return True

    def _type_of(self, column: int) -> DataType:
        return self._types[column]

    def _data_of(self, column: int) -> List[Any]:
        return self._cached_data[column]

    def _display_role(self, row: int, column: int) -> str:
        """Returns a text representation of each cell value."""
        try:
            return self._data_of(column)[row]

        except IndexError:
            return None

    def _type_role(self, row: int, column: int):
        """Returns the datatype associated to the row value."""
        try:
            return self._type_of(column)

        except IndexError:
            return None


DatasetTableModelFactory = providers.Factory(DatasetTableModel)
