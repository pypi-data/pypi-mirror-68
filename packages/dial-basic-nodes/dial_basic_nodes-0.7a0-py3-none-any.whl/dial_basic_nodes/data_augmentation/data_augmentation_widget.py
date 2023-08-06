# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

import re
from typing import Callable, List, Optional, Tuple

import dependency_injector.providers as providers
import numpy as np
import tensorflow as tf
from dial_core.datasets import Dataset, TTVSets
from dial_core.utils import log
from PySide2.QtCore import Signal
from PySide2.QtWidgets import (
    QCheckBox,
    QGroupBox,
    QHBoxLayout,
    QLineEdit,
    QVBoxLayout,
    QWidget,
)

LOGGER = log.get_logger(__name__)


class OperationGroup(QGroupBox):
    operation_changed = Signal()

    def __init__(self, title: str, parent: "QWidget" = None):
        super().__init__(title, parent)

        self._enabled_status_checkbox = QCheckBox("Enabled")
        self._enabled_status_checkbox.setChecked(False)

        self._main_layout = QVBoxLayout()

        self._central_widget = QWidget()
        self._central_widget.setEnabled(self._enabled_status_checkbox.isChecked())

        self._central_layout = QVBoxLayout()
        self._central_widget.setLayout(self._central_layout)

        self._main_layout.addWidget(self._enabled_status_checkbox)
        self._main_layout.addWidget(self._central_widget)

        self.setLayout(self._main_layout)

        self._enabled_status_checkbox.stateChanged.connect(self._changeEnabled)

    def get_operation(self) -> Callable:
        raise NotImplementedError()

    def fill_values_from_dataset(self, dataset: "Dataset"):
        pass

    def is_checked(self) -> bool:
        return self._enabled_status_checkbox.isChecked()

    def addWidget(self, widget: "QWidget"):
        self._central_layout.addWidget(widget)

    def _changeEnabled(self, state: int):
        LOGGER.debug("%s state changed to: %s", self, self.is_checked())

        self._enabled_status_checkbox.setChecked(state)
        self._central_widget.setEnabled(state)

        self.operation_changed.emit()


class ResizeOperation(OperationGroup):
    def __init__(self, parent: "QWidget" = None):
        super().__init__("Target Size")

        self._target_size_textbox = QLineEdit()

        self.addWidget(self._target_size_textbox)

        self._target_size_textbox.editingFinished.connect(
            lambda: self.set_target_size(self._target_size_textbox.text())
        )

    def get_operation(self) -> Callable:
        def resize_operation(image):
            return image.resize(self.get_target_size())

        return resize_operation

    def fill_values_from_dataset(self, dataset: "Dataset"):
        input_shape = dataset.input_shape
        LOGGER.debug("Setting input shape of %s to %s", dataset, input_shape)

        self.set_target_size(str(input_shape))

    def get_target_size(self) -> Tuple[int, int]:
        return tuple(
            map(int, re.sub("[()]", "", self._target_size_textbox.text()).split(","))
        )

    def set_target_size(self, new_target_size: str):
        tuple_string_list = re.sub("[()]", "", str(new_target_size)).split(",")

        processed_tuple = tuple(
            [int(element) if element else None for element in tuple_string_list]
        )

        if len(processed_tuple) > 2:
            LOGGER.warning(
                (
                    "Target size must be of length 2. Current: %s. ",
                    "Using only first two values.",
                ),
                processed_tuple,
            )

            processed_tuple = processed_tuple[0:2]

        print(">>>>")

        self._target_size_textbox.setText(str(processed_tuple))

        LOGGER.debug("New target size: %s", self.get_target_size())

        self.operation_changed.emit()


class OperationsColumn(QWidget):
    operations_updated = Signal()

    def __init__(self, parent: "QWidget" = None):
        super().__init__(parent)

        self._operation_widgets = []

        # Target Size -> Resize the Input Image
        self._resize_operation = ResizeOperation()
        self._resize_operation.operation_changed.connect(
            lambda: self.operations_updated.emit()
        )

        self._operation_widgets.append(self._resize_operation)

        self._main_layout = QVBoxLayout()
        self._main_layout.addWidget(self._resize_operation)

        self.setLayout(self._main_layout)

    def fill_values_from_dataset(self, dataset: "Dataset"):
        for widget in self._operation_widgets:
            widget.fill_values_from_dataset(dataset)

    def get_operations(self) -> List[Callable]:
        operations = []

        for widget in self._operation_widgets:
            if widget.is_checked():
                operations.append(widget.get_operation())

        return operations


class DataAugmentationWidget(QWidget):
    operations_updated = Signal()

    def __init__(self, parent: "QWidget" = None):
        super().__init__(parent)

        # Components
        self._ttv: Optional["TTVSets"] = None
        self._previous_operations: List[Callable] = []

        # Initialize widgets
        self._operations_column = OperationsColumn()

        self._operations_column.operations_updated.connect(self.update_operations)

        # Setup Layout
        self._main_layout = QHBoxLayout()
        self._main_layout.setContentsMargins(0, 0, 0, 0)
        self._main_layout.addWidget(self._operations_column)

        self.setLayout(self._main_layout)

    def set_ttv(self, ttv: "TTVSets"):
        self._ttv = ttv

        for dataset in (ttv.train, ttv.test, ttv.validation):
            if dataset is None:
                continue

            LOGGER.debug("Updating widget values with %s", self)
            self._operations_column.fill_values_from_dataset(dataset)
            break

        self.update_operations()

    def set_previous_operations(self, operations: List[Callable]):
        self._previous_operations = operations

        self.update_operations()

    def get_augmented_ttv(self):
        return self._ttv

    def update_operations(self):
        if not self._ttv:
            return

        # Instead of storing several image augmentation operations, merge all them into
        # one big operation that only transforms the array to image once.
        def grouped_augmentation_operation(data: "np.ndarray"):
            try:
                image = tf.keras.preprocessing.image.array_to_img(data)

                for f in self._operations_column.get_operations():
                    try:
                        image = f(image)

                    except Exception as err:
                        LOGGER.exception(
                            (
                                "Error during the DataAgumentation function %s.",
                                " Skipped... Error: %s",
                            ),
                            f,
                            err,
                        )

                return tf.keras.preprocessing.image.img_to_array(image)

            except Exception as err:
                LOGGER.exception(
                    "Error during the Grouped DataAgumentation. Not applied. %s", err,
                )

                return data

        for dataset in (self._ttv.train, self._ttv.test, self._ttv.validation):
            if dataset:
                dataset.x_type.transformations = [
                    grouped_augmentation_operation
                ] + self._previous_operations

        LOGGER.debug(self._ttv.train.x_type.transformations)

        self.operations_updated.emit()


DataAugmentationWidgetFactory = providers.Factory(DataAugmentationWidget)
