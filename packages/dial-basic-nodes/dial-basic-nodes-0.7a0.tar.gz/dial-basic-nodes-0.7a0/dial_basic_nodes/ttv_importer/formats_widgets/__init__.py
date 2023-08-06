# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from .categorical_images_widget import (
    CategoricalImagesWidget,
    CategoricalImagesWidgetFactory,
)
from .npz_widget import NpzWidget, NpzWidgetFactory

__all__ = [
    "NpzWidget",
    "NpzWidgetFactory",
    "CategoricalImagesWidget",
    "CategoricalImagesWidgetFactory",
]
