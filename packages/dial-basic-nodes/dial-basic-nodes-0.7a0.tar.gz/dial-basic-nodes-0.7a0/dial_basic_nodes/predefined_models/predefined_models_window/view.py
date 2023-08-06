# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from typing import TYPE_CHECKING

import dependency_injector.providers as providers
from PySide2.QtWidgets import QListView

if TYPE_CHECKING:
    from PySide2.QtWidgets import QWidget


class PredefinedModelsView(QListView):
    def __init__(self, parent: "QWidget" = None):
        super().__init__(parent)

    def __reduce__(self):
        return (PredefinedModelsView, ())


PredefinedModelsViewFactory = providers.Factory(PredefinedModelsView)
