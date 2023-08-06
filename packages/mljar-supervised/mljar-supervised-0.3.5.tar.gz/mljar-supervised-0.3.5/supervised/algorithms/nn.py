################################################################################
# switch off tf warnings
import os

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"
import os
import sys

stderr = sys.stderr
sys.stderr = open(os.devnull, "w")
import keras

sys.stderr = stderr
################################################################################
# set seed for reproducibility
# however in case of running on multiple CPU or GPU there is no reproducibility
import numpy as np
import tensorflow as tf
import random as rn

np.random.seed(42)
rn.seed(12345)
from keras import backend as K

tf.set_random_seed(1234)
tf.logging.set_verbosity(tf.logging.ERROR)
################################################################################
import logging
import copy
import numpy as np
import pandas as pd
import os
import keras

from keras.optimizers import SGD
from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras.models import model_from_json
from keras.utils import to_categorical

from supervised.algorithms.algorithm import BaseAlgorithm
from supervised.algorithms.registry import AlgorithmsRegistry
from supervised.algorithms.registry import BINARY_CLASSIFICATION
from supervised.algorithms.registry import MULTICLASS_CLASSIFICATION

from supervised.utils.config import LOG_LEVEL

logger = logging.getLogger(__name__)
logger.setLevel(LOG_LEVEL)


class NeuralNetworkAlgorithm(BaseAlgorithm):

    algorithm_name = "Neural Network"
    algorithm_short_name = "NN"

    def __init__(self, params):
        super(NeuralNetworkAlgorithm, self).__init__(params)

        self.library_version = keras.__version__

        self.rounds = additional.get("one_step", 10)
        self.max_iters = additional.get("max_steps", 1)
        self.learner_params = {
            "dense_layers": params.get("dense_layers"),
            "dense_1_size": params.get("dense_1_size"),
            "dense_2_size": params.get("dense_2_size"),
            "dense_3_size": params.get("dense_3_size"),
            "dropout": params.get("dropout"),
            "learning_rate": params.get("learning_rate"),
            "momentum": params.get("momentum"),
            "decay": params.get("decay"),
        }
        self.model = None  # we need input data shape to construct model
        logger.debug("NeuralNetworkAlgorithm __init__")

    def create_model(self, input_dim):
        self.model = Sequential()
        for i in range(self.learner_params.get("dense_layers")):
            self.model.add(
                Dense(
                    self.learner_params.get("dense_{}_size".format(i + 1)),
                    activation="relu",
                    input_dim=input_dim,
                )
            )
            if self.learner_params.get("dropout"):
                self.model.add(Dropout(rate=self.learner_params.get("dropout")))

        if "num_class" in self.params:
            self.model.add(Dense(self.params["num_class"], activation="softmax"))
        else:
            self.model.add(Dense(1, activation="sigmoid"))

        sgd_opt = SGD(
            lr=self.learner_params.get("learning_rate"),
            momentum=self.learner_params.get("momentum"),
            decay=self.learner_params.get("decay"),
            nesterov=True,
        )

        if "num_class" in self.params:
            self.model.compile(
                optimizer=sgd_opt, loss="categorical_crossentropy", metrics=["accuracy"]
            )
        else:
            self.model.compile(
                optimizer=sgd_opt, loss="binary_crossentropy", metrics=["accuracy"]
            )

    def update(self, update_params):
        pass

    def fit(self, X, y):
        logger.debug("NNLearner.fit")

        if self.model is None:
            self.create_model(input_dim=X.shape[1])

        # rounds for learning are incremental
        # if "num_class" in self.params:
        #    self.model.fit(
        #        X, to_categorical(y), batch_size=256, epochs=self.rounds, verbose=False
        #    )
        # else:

        self.model.fit(X, y, batch_size=256, epochs=self.rounds, verbose=False)
        logger.debug("NNLearner.fit end")

    def predict(self, X):
        if "num_class" in self.params:
            return self.model.predict(X)
        return np.ravel(self.model.predict(X))

    def copy(self):
        return copy.deepcopy(self)

    def save(self):

        self.model.save_weights(self.model_file_path)

        json_desc = {
            "library_version": self.library_version,
            "algorithm_name": self.algorithm_name,
            "algorithm_short_name": self.algorithm_short_name,
            "uid": self.uid,
            "model_file": self.model_file,
            "model_file_path": self.model_file_path,
            "params": self.params,
            "model_architecture_json": self.model.to_json(),
        }

        logger.debug("NeuralNetworkLearner save model to %s" % self.model_file_path)
        return json_desc

    def load(self, json_desc):

        self.library_version = json_desc.get("library_version", self.library_version)
        self.algorithm_name = json_desc.get("algorithm_name", self.algorithm_name)
        self.algorithm_short_name = json_desc.get(
            "algorithm_short_name", self.algorithm_short_name
        )
        self.uid = json_desc.get("uid", self.uid)
        self.model_file = json_desc.get("model_file", self.model_file)
        self.model_file_path = json_desc.get("model_file_path", self.model_file_path)
        self.params = json_desc.get("params", self.params)
        model_json = json_desc.get("model_architecture_json")

        logger.debug("NeuralNetworkLearner load model from %s" % self.model_file_path)

        self.model = model_from_json(model_json)
        self.model.load_weights(self.model_file_path)

    def importance(self, column_names, normalize=True):
        return None


nn_params = {
    "dense_layers": [1, 2, 3],
    "dense_1_size": [4, 8, 16, 32, 64, 128],
    "dense_2_size": [4, 8, 16, 32, 64],
    "dense_3_size": [4, 8, 16, 32],
    "dropout": [0, 0.25, 0.5, 0.75],
    "learning_rate": [0.005, 0.01, 0.05, 0.1, 0.2],
    "momentum": [0.85, 0.9, 0.95],
    "decay": [0.0001, 0.001, 0.01],
}

additional = {
    "one_step": 10,
    "train_cant_improve_limit": 5,
    "max_steps": 1000,
    "max_rows_limit": None,
    "max_cols_limit": None,
}
required_preprocessing = [
    "missing_values_inputation",
    "convert_categorical",
    "scale",
    "target_as_integer",
]

AlgorithmsRegistry.add(
    BINARY_CLASSIFICATION,
    NeuralNetworkAlgorithm,
    nn_params,
    required_preprocessing,
    additional,
)

required_preprocessing = [
    "missing_values_inputation",
    "convert_categorical",
    "scale",
    "target_as_one_hot",
]
AlgorithmsRegistry.add(
    MULTICLASS_CLASSIFICATION,
    NeuralNetworkAlgorithm,
    nn_params,
    required_preprocessing,
    additional,
)
