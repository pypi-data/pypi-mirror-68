# Author: Simon Blanke
# Email: simon.blanke@yahoo.com
# License: MIT License

__version__ = "0.2.1"
__license__ = "MIT"


from .hypermemory import Hypermemory
from .memory_helper import (
    delete_model,
    delete_model_dataset,
    connect_model_IDs,
    split_model_IDs,
    reset_memory,
    get_best_model,
)

__all__ = [
    "delete_model",
    "delete_model_dataset",
    "connect_model_IDs",
    "split_model_IDs",
    "reset_memory",
    "Hypermemory",
    "get_best_model",
]
