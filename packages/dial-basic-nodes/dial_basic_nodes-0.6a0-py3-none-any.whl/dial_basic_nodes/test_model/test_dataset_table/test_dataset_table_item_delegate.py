# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from typing import TYPE_CHECKING

from PySide2.QtGui import QBrush, QColor

from dial_basic_nodes.utils.dataset_table import DatasetTableItemDelegate

from .test_dataset_table_model import TestDatasetTableModel

if TYPE_CHECKING:
    from PySide2.QtCore import QModelIndex
    from PySide2.QtGui import QPainter
    from PySide2.QtWidgets import QStyleOptionViewItem
    from PySide2.QtCore import QObject


class TestDatasetTableItemDelegate(DatasetTableItemDelegate):
    def __init__(self, parent: "QObject" = None):
        super().__init__(parent)

        self._correct_brush = QBrush(QColor("#e8ffe0"))
        self._incorrect_brush = QBrush(QColor("#ffe3e0"))

    def paint(
        self, painter: "QPainter", option: "QStyleOptionViewItem", index: "QModelIndex"
    ):
        predicted_data = index.data(TestDatasetTableModel.PredictionResultRole)

        if predicted_data is not None:
            painter.fillRect(
                option.rect,
                self._correct_brush if predicted_data else self._incorrect_brush,
            )

        super().paint(painter, option, index)
