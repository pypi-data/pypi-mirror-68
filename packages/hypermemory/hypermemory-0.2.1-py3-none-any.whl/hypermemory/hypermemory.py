# Author: Simon Blanke
# Email: simon.blanke@yahoo.com
# License: MIT License

import numpy as np


from .memory_load import MemoryLoad
from .memory_dump import MemoryDump


class Hypermemory:
    def __init__(self, X, y, model, search_space, path=None):
        self.memory_dict = None
        self.meta_data_found = False
        self.n_dims = None

        self._load_ = MemoryLoad(X, y, model, search_space, path=path)
        self._dump_ = MemoryDump(X, y, model, search_space, path=path)

    def load(self):
        self.memory_dict = self._load_._load_memory()
        self.meta_data_found = self._load_.meta_data_found

        self.score_best = self._load_.score_best
        self.pos_best = self._load_.pos_best

        return self.memory_dict

    def dump(self, memory, main_args=None):
        self._dump_._save_memory(memory, main_args=main_args)

    def _get_para(self):
        if self.memory_dict is None:
            print("Error")
            return
        para_pd, metrics_pd = self._dump_._get_opt_meta_data(self.memory_dict)

        return para_pd.values, np.expand_dims(metrics_pd["score"].values, axis=1)

    """
    def _get_hash(self, object):
        return hashlib.sha1(object).hexdigest()

    def _get_func_str(self, func):
        return inspect.getsource(func)

    def _obj2hash(self):
        obj2hash_dict = {}
        para_hash_list = self._get_para_hash_list()

        for para_hash in para_hash_list:
            obj = self._read_dill(para_hash)
            obj2hash_dict[para_hash] = obj

        return obj2hash_dict
    """
