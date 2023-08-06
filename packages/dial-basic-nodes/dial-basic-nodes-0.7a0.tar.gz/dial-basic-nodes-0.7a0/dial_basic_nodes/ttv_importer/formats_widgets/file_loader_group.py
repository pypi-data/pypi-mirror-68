# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from dial_core.utils import log
from PySide2.QtWidgets import (
    QFileDialog,
    QGroupBox,
    QHBoxLayout,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

LOGGER = log.get_logger(__name__)


class FileLoaderGroup(QGroupBox):
    def __init__(
        self,
        title: str,
        parent: "QWidget" = None,
        filter: str = "",
        pick_directories: bool = False,
    ):
        super().__init__(title, parent)

        self._file_picker_dialog = QFileDialog(
            caption=f'Picking a "{title}" file...', filter=filter
        )
        self._file_picker_dialog.setFileMode(
            QFileDialog.DirectoryOnly if pick_directories else QFileDialog.ExistingFile
        )

        self._pick_file_text = QLineEdit()
        self._pick_file_text.setReadOnly(True)
        self._pick_file_text.setPlaceholderText("Path...")
        self._pick_file_button = QPushButton("Load")

        self._pick_file_layout = QHBoxLayout()
        self._pick_file_layout.addWidget(self._pick_file_text)
        self._pick_file_layout.addWidget(self._pick_file_button)

        self._main_layout = QVBoxLayout()
        self._main_layout.addLayout(self._pick_file_layout)

        self.setLayout(self._main_layout)

        self._pick_file_button.clicked.connect(self._load_from_filesystem)

    @property
    def layout(self) -> "QVBoxLayout":
        return self._main_layout

    @property
    def path(self) -> str:
        return self._pick_file_text.text()

    @path.setter
    def path(self, path: str):
        self._pick_file_text.setText(path)

    def _load_from_filesystem(self):
        LOGGER.debug("Picking file...")

        if self._file_picker_dialog.exec():
            self._pick_file_text.setText(self._file_picker_dialog.selectedFiles()[0])
