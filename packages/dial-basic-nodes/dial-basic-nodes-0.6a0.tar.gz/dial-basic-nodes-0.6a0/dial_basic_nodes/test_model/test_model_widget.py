# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from typing import Optional

import dependency_injector.providers as providers
from dial_core.datasets import Dataset
from dial_core.utils import log
from PySide2.QtCore import QSize
from PySide2.QtWidgets import QPushButton, QVBoxLayout, QWidget
from tensorflow import keras

from .test_dataset_table import TestDatasetTableWidgetFactory

LOGGER = log.get_logger(__name__)


class TestModelWidget(QWidget):
    # Top: Data about the current model.
    # (Name, Training accuracy? Dunno)
    # Bottom: List with all the training dataset things
    # Three columns: Class, Predicted, Expected
    # Accuracy of the test
    # Possibility to filter and see only the failed tests, for example.
    # When the button (Check tests) is clicked, update the predicted values.
    def __init__(self, test_dataset_widget, parent: "QWidget" = None):
        super().__init__(parent)

        # Componentes
        self._trained_model: Optional["keras.models.Model"] = None

        # Widgets
        self._test_dataset_widget = test_dataset_widget
        self._predict_button = QPushButton("Predict values")

        self._main_layout = QVBoxLayout()
        self._main_layout.setContentsMargins(0, 0, 0, 0)
        self._main_layout.addWidget(self._predict_button)
        self._main_layout.addWidget(self._test_dataset_widget)

        self.setLayout(self._main_layout)

        # Connections
        self._predict_button.clicked.connect(self.predict_values)

    def set_test_dataset(self, test_dataset: "Dataset"):
        LOGGER.debug("Test dataset set: %s", test_dataset)
        self._test_dataset_widget.load_dataset(test_dataset)

    def set_trained_model(self, model: "keras.models.Model"):
        LOGGER.debug("Compiled model set: %s", model)
        self._trained_model = model

    def predict_values(self):
        if self._trained_model is None:
            LOGGER.debug("No trained model selected.")
            return

        predicted_data = self._trained_model.predict(self._test_dataset_widget.dataset)
        self._test_dataset_widget.set_predict_values(predicted_data)

        LOGGER.debug(
            "Predicting %s with %s",
            self._test_dataset_widget.dataset,
            self._trained_model,
        )

    def sizeHint(self) -> "QSize":
        """Optimal size for visualizing the widget."""
        return QSize(500, 300)

    def __reduce__(self):
        return (TestModelWidget, (self._test_dataset_widget))


TestModelWidgetFactory = providers.Factory(
    TestModelWidget, test_dataset_widget=TestDatasetTableWidgetFactory
)
