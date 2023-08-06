# Author: Simon Blanke
# Email: simon.blanke@yahoo.com
# License: MIT License

import time

from sklearn.datasets import load_iris
from sklearn.model_selection import cross_val_score
from sklearn.tree import DecisionTreeClassifier
from hypermemory import Hypermemory

data = load_iris()
X, y = data.data, data.target


def model(para, X, y):
    dtc = DecisionTreeClassifier(
        max_depth=para["max_depth"], min_samples_split=para["min_samples_split"],
    )
    scores = cross_val_score(dtc, X, y, cv=3)

    return scores.mean()


search_space = {
    "max_depth": range(1, 5),
    "min_samples_split": range(2, 5),
}


def test_():
    memory_in = {
        b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00": {
            "score": 0.6274204028589994,
            "eval_time": 0.005737781524658203,
        },
        b"\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00": {
            "score": 0.6274204028589994,
            "eval_time": 0.007668018341064453,
        },
        b"\x01\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00": {
            "score": 0.6274204028589994,
            "eval_time": 0.011501789093017578,
        },
    }

    mem = Hypermemory(X, y, model, search_space)
    mem.dump(memory_in)
    memory_out = mem.load()

    assert memory_in == memory_out
