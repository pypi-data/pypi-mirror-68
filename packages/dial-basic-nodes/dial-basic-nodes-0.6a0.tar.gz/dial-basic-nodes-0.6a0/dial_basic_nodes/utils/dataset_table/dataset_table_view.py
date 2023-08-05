# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

import dependency_injector.providers as providers
from PySide2.QtCore import Qt
from PySide2.QtWidgets import QAbstractItemView, QHeaderView, QTableView, QWidget

from .dataset_table_item_delegate import DatasetTableItemDelegate


class DatasetTableView(QTableView):
    def __init__(self, parent: "QWidget" = None):
        super().__init__(parent)

        # Headers
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.verticalHeader().setSectionResizeMode(QHeaderView.Interactive)

        self.horizontalHeader().setContextMenuPolicy(Qt.CustomContextMenu)
        # self.horizontalHeader().customContextMenuRequested.connect(
        #     self.__show_header_datatype_selection_menu
        # )

        # Configuration
        self.setSelectionBehavior(QAbstractItemView.SelectRows)

        self.setItemDelegate(DatasetTableItemDelegate())


DatasetTableViewFactory = providers.Factory(DatasetTableView)
DatasetTableViewFactory = providers.Factory(DatasetTableView)
