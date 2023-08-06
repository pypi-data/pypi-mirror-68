# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from enum import Enum
from typing import Dict, List, Optional

import dependency_injector.providers as providers
from dial_core.datasets import TTVSets
from dial_core.utils import log
from PySide2.QtCore import QObject, QSize, Qt, QThread, Signal
from PySide2.QtWidgets import (
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QPlainTextEdit,
    QProgressBar,
    QPushButton,
    QVBoxLayout,
    QWidget,
)
from tensorflow import keras
from tensorflow.keras.callbacks import Callback
from tensorflow.keras.layers import Input
from tensorflow.keras.models import Model

LOGGER = log.get_logger(__name__)


class SignalsCallback(keras.callbacks.Callback, QObject):
    epoch_begin = Signal(int, dict)
    epoch_end = Signal(int, dict)
    train_batch_end = Signal(int, dict)
    train_end = Signal(dict)

    def __init__(self, batches_between_updates: int = 100):
        keras.callbacks.Callback.__init__(self)
        QObject.__init__(self)

        self.batches_between_updates = batches_between_updates

    def on_train_batch_end(self, batch: int, logs=None):
        if batch % self.batches_between_updates == 0:
            self.train_batch_end.emit(batch, logs)

    def on_train_end(self, logs=None):
        self.train_end.emit(logs)

    def on_epoch_begin(self, epoch: int, logs=None):
        self.epoch_begin.emit(epoch, logs)

    def on_epoch_end(self, epoch: int, logs=None):
        self.epoch_end.emit(epoch, logs)

    def stop_model(self):
        self.model.stop_training = True


class FitWorker(QThread):
    def __init__(self, model, train_dataset, hyperparameters, callbacks):
        super().__init__()

        self._model = model
        self._train_dataset = train_dataset
        self._hyperparameters = hyperparameters
        self._callbacks = callbacks

    def run(self):
        self._model.fit(
            self._train_dataset,
            epochs=self._hyperparameters["epochs"],
            callbacks=self._callbacks,
        )


class TrainingConsoleWidget(QWidget):
    """The TrainingConsoleWidget provides a widget for controlling the training status
    of a model, in a simple way. (Analog of the console output in Keras, but with a few
    more options).

    It also can save and show an history of the last trained models.
    """

    training_started = Signal()
    training_stopped = Signal()

    class TrainingStatus(Enum):
        Running = 1
        Stopped = 2
        Not_Compiled = 3

    def __init__(self, parent: "QWidget" = None):
        super().__init__(parent)

        # Components
        self._pretrained_model: Optional["keras.models.Model"] = None
        self._ttv: Optional["TTVSets"] = None
        self._hyperparameters: Optional[Dict] = None
        self._callbacks: List[Callback] = []

        self._trained_model: Optional["keras.models.Model"] = None

        # Widgets
        self._start_training_button = QPushButton("Start training")
        self._stop_training_button = QPushButton("Stop training")

        self._buttons_layout = QHBoxLayout()
        self._buttons_layout.addWidget(self._start_training_button)
        self._buttons_layout.addWidget(self._stop_training_button)

        self._status_label = QLabel()

        self._batch_progress_bar = QProgressBar()
        self._epoch_progress_bar = QProgressBar()

        self.training_output_textbox = QPlainTextEdit()
        self.training_output_textbox.setReadOnly(True)

        console_output_group = QGroupBox("Console output")
        console_output_layout = QVBoxLayout()
        console_output_layout.setContentsMargins(0, 0, 0, 0)
        console_output_layout.addWidget(self.training_output_textbox)
        console_output_group.setLayout(console_output_layout)

        self._main_layout = QVBoxLayout()
        self._main_layout.addLayout(self._buttons_layout)
        self._main_layout.addWidget(self._status_label, Qt.AlignRight)
        self._main_layout.addWidget(console_output_group)
        self._main_layout.addWidget(self._batch_progress_bar)
        self._main_layout.addWidget(self._epoch_progress_bar)
        self.setLayout(self._main_layout)

        # Connections
        self._start_training_button.clicked.connect(self.start_training)
        self._stop_training_button.clicked.connect(self.stop_training)

        # Inner workings
        self.training_status = self.TrainingStatus.Not_Compiled
        self._training_thread = None

    @property
    def training_status(self):
        """Returns the current status of the training (Running, Stopped...)"""
        return self._training_status

    @training_status.setter
    def training_status(self, new_status):
        """Changes the training status.

        Doing so will update the interface accordingly.
        """
        self._training_status = new_status

        if self._training_status == self.TrainingStatus.Running:
            self._start_training_button.setEnabled(False)
            self._stop_training_button.setEnabled(True)
            self._status_label.setText("Running")
            self.start_training

        elif self._training_status == self.TrainingStatus.Stopped:
            self._start_training_button.setEnabled(True)
            self._stop_training_button.setEnabled(False)
            self._status_label.setText("Stopped")

        elif self._training_status == self.TrainingStatus.Not_Compiled:
            self._start_training_button.setEnabled(True)
            self._stop_training_button.setEnabled(False)
            self._status_label.setText("Not Compiled")

    def set_ttv(self, ttv: "TTVSets"):
        """Sets the Train/Test/Validation models used for training."""
        self._ttv = ttv

    def set_pretrained_model(self, pretrained_model: "Model"):
        """Sets a new pretrained model for training."""
        self._pretrained_model = pretrained_model

        self.training_status = self.TrainingStatus.Not_Compiled

    def set_hyperparameters(self, hyperparameters: Dict):
        """Sets new hyperparameters for training."""
        self._hyperparameters = hyperparameters

        self.training_status = self.TrainingStatus.Not_Compiled

    def set_callbacks(self, callbacks: List[Callback]):
        self._callbacks = callbacks

    def get_trained_model(self):
        """Returns the model after it has been trained."""
        return self._trained_model

    def compile_model(self):
        """Compile the model with the passed hyperparameters. The dataset is needed for
        the input shape."""
        LOGGER.info("Starting to compile the model...")

        if not self._is_input_ready():
            return False

        # Create a new model based on the pretrained one, but with a new InputLayer
        # compatible with the dataset
        if self._pretrained_model.layers[0].__class__.__name__ != "InputLayer":
            input_layer = Input(self._ttv.train.input_shape)

            output = self._pretrained_model(input_layer)
            self._trained_model = Model(input_layer, output)
        else:
            self._trained_model = self._pretrained_model

        try:
            self._trained_model.compile(
                optimizer=self._hyperparameters["optimizer"],
                loss=self._hyperparameters["loss_function"],
                metrics=["accuracy"],
            )

            self._trained_model.summary()

            LOGGER.info("Model compiled successfully!!")

            self.training_status = self.TrainingStatus.Stopped

            return True

        except Exception as err:
            LOGGER.exception("Model Compiling error: ", err)

            self.training_output_textbox.setPlainText(
                "> Error while compiling the model:\n", str(err)
            )

        return False

    def start_training(self):
        """Starts the training on a new thread."""
        if self.training_status == self.TrainingStatus.Not_Compiled:
            successfully_compiled = self.compile_model()

            if not successfully_compiled:
                LOGGER.info("Couldn't compile model. Training not started.")
                return

        total_train_batches = len(self._ttv.train)
        total_train_epochs = self._hyperparameters["epochs"]

        self._batch_progress_bar.setMaximum(total_train_batches)
        self._epoch_progress_bar.setMaximum(total_train_epochs)
        self._epoch_progress_bar.setValue(0)
        self.training_output_textbox.clear()

        def epoch_begin_update(epoch: int, logs):
            message = f"==== Epoch {epoch + 1}/{total_train_epochs} ===="

            LOGGER.info(message)
            self.training_output_textbox.appendPlainText(message)
            self._epoch_progress_bar.setValue(epoch)

        def batch_end_update(batch: int, logs):
            # Update progress
            self._batch_progress_bar.setValue(batch)

            # Log metrics on console
            message = f"{batch}/{total_train_batches}"

            for (k, v) in list(logs.items()):
                message += f" - {k}: {v:.4f}"

            LOGGER.info(message)
            self.training_output_textbox.appendPlainText(message)

        def train_end_update(logs):
            # Put the progress bar at 100% when the training ends
            self._batch_progress_bar.setValue(self._batch_progress_bar.maximum())
            self._epoch_progress_bar.setValue(self._epoch_progress_bar.maximum())

            # Stop the training
            self.stop_training()

        # Connect callbacks
        signals_callback = SignalsCallback()
        signals_callback.epoch_begin.connect(epoch_begin_update)
        signals_callback.train_batch_end.connect(batch_end_update)
        signals_callback.train_end.connect(train_end_update)

        self.training_stopped.connect(signals_callback.stop_model)

        print(self._callbacks)
        # log_dir = "logs/fit/" + datetime.datetime.now().strftime("%Y_%m_%d-%H_%M_%S")

        # tb = program.TensorBoard()
        # tb.configure(argv=[None, "--logdir", log_dir])
        # url = tb.launch()
        # print("Launched Tensorboard instance in:", url)

        # tf_callback=tf.keras.callbacks.TensorBoard(log_dir=log_dir, histogram_freq=1)
        # tf_callback.set_model(self._trained_model)

        # Start training
        self._fit_worker = FitWorker(
            self._trained_model,
            self._ttv.train,
            self._hyperparameters,
            callbacks=[signals_callback] + self._callbacks,
        )

        self.training_status = self.TrainingStatus.Running
        self._fit_worker.start()

        self.training_started.emit()

    def stop_training(self):
        """Stops the training."""
        self.training_status = self.TrainingStatus.Stopped

        self.training_stopped.emit()

    def _is_input_ready(self) -> bool:
        """Checks if the input values used for training (model, dataset,
        hyperparameters...) are valid."""
        message = ""

        if not self._ttv.train:
            message += "> Training dataset not specified\n"

        if not self._pretrained_model:
            message += "> Model not specified.\n"

        if not self._hyperparameters:
            message += "> Hyperparameters not specified.\n"

        if message:
            self.training_output_textbox.setPlainText(message)
            LOGGER.info(message)
            return False

        return True

    def sizeHint(self) -> "QSize":
        """Returns the expected size of the widget."""
        return QSize(500, 300)

    def __reduce__(self):
        return (TrainingConsoleWidget, ())


TrainingConsoleWidgetFactory = providers.Factory(TrainingConsoleWidget)
