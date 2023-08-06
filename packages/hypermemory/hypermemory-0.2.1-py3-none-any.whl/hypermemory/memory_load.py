# Author: Simon Blanke
# Email: simon.blanke@yahoo.com
# License: MIT License

import os
import json
import glob

import numpy as np
import pandas as pd

from functools import partial

from .memory_io import MemoryIO
from .utils import model_id
from .paths import model_path


def apply_tobytes(df):
    return df.values.tobytes()


class MemoryLoad(MemoryIO):
    def __init__(self, X, y, model, search_space, path):
        super().__init__(X, y, model, search_space, path)

        self.pos_best = None
        self.score_best = -np.inf

        self.meta_data_found = False

        self.con_ids = []

        if not os.path.exists(self.meta_path + "model_connections.json"):
            with open(self.meta_path + "model_connections.json", "w") as f:
                json.dump({}, f, indent=4)

        with open(self.meta_path + "model_connections.json") as f:
            self.model_con = json.load(f)

        model_id_ = model_id(self.model)
        if model_id_ in self.model_con:
            self._get_id_list(self.model_con[model_id_])
        else:
            self.con_ids = [model_id_]

        self.con_ids = set(self.con_ids)

    def _get_id_list(self, id_list):
        self.con_ids = self.con_ids + id_list

        for id in id_list:
            id_list_new = self.model_con[id]

            if set(id_list_new).issubset(self.con_ids):
                continue

            self._get_id_list(id_list_new)

    def _load_memory(self):
        para, score = self._read_func_metadata(self.model)
        if para is None or score is None:
            return {}

        # _verb_.load_samples(para)

        memory_dict = self._load_data_into_memory(para, score)
        self.n_dims = len(para.columns)

        return memory_dict

    def apply_index(self, pos_key, df):
        return (
            self.search_space[pos_key].index(df)
            if df in self.search_space[pos_key]
            else None
        )

    def _read_func_metadata(self, model_func):
        paths = self._get_func_data_names()

        meta_data_list = []
        for path in paths:
            meta_data = pd.read_csv(path)
            meta_data_list.append(meta_data)
            self.meta_data_found = True

        if len(meta_data_list) > 0:
            meta_data = pd.concat(meta_data_list, ignore_index=True)

            # column_names = meta_data.columns
            # score_name = [name for name in column_names if self.score_col_name in name]

            para = meta_data[self.para_names]
            score = meta_data[self.score_col_name]

            # _verb_.load_meta_data()
            return para, score

        else:
            # _verb_.no_meta_data(model_func)
            return None, None

    def _get_func_data_names(self):
        paths = []
        for id in self.con_ids:
            paths = paths + glob.glob(
                self.meta_path + model_path(id) + self.meta_data_name
            )

        return paths

    def para2pos(self, paras):
        paras = paras[self.para_names]
        pos = paras.copy()

        for pos_key in self.search_space:
            apply_index = partial(self.apply_index, pos_key)
            pos[pos_key] = paras[pos_key].apply(apply_index)

        pos.dropna(how="any", inplace=True)
        pos = pos.astype("int64")

        return pos

    def _load_data_into_memory(self, paras, scores):
        paras = paras.replace(self.hash2obj)
        pos = self.para2pos(paras)

        if len(pos) == 0:
            return

        df_temp = pd.DataFrame()
        df_temp["pos_str"] = pos.apply(apply_tobytes, axis=1)
        df_temp[["score", "eval_time"]] = scores

        memory_dict = df_temp.set_index("pos_str").to_dict("index")

        scores = np.array(scores)
        pos = np.array(pos)

        idx = np.argmax(scores)
        self.score_best = scores[idx][0]  # get score but not eval_time
        self.pos_best = pos[idx]

        return memory_dict
