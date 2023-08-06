# Author: Simon Blanke
# Email: simon.blanke@yahoo.com
# License: MIT License

import os
import json
import dill
import inspect

import numpy as np
import pandas as pd

from .memory_io import MemoryIO
from .dataset_features import get_dataset_features
from .utils import object_hash


class MemoryDump(MemoryIO):
    def __init__(self, X, y, model, search_space, path):
        super().__init__(X, y, model, search_space, path)

    def _save_memory(self, memory_dict, main_args):
        self.memory_dict = memory_dict

        # Save meta_data
        path = self._get_file_path(self.model)
        meta_data = self._collect(memory_dict)

        if meta_data is None:
            return

        meta_data["run"] = self.datetime
        self._save_toCSV(meta_data, path)

        # Save function
        obj_func_path = self.model_path + "objective_function.pkl"

        with open(obj_func_path, "wb") as pickle_file:
            dill.dump(self.model, pickle_file)

        # Save search space
        search_space_path = self.model_path + "search_space.pkl"

        with open(search_space_path, "wb") as pickle_file:
            dill.dump(self.search_space, pickle_file)

        # Save data_features
        data_features = get_dataset_features(self.X, self.y)

        if not os.path.exists(self.dataset_info_path):
            os.makedirs(self.dataset_info_path, exist_ok=True)

        with open(self.dataset_info_path + "data_features.json", "w") as f:
            json.dump(data_features, f, indent=4)

        if main_args:
            run_data = {
                "random_state": main_args.random_state,
                "max_time": main_args.random_state,
                "n_iter": main_args.n_iter,
                "optimizer": main_args.optimizer,
                "n_jobs": main_args.n_jobs,
                # "eval_time": main_args.eval_time,
                # "opt_time": main_args.opt_time,
                # "total_time": main_args.total_time,
            }

            with open(self.date_path + "run_data.json", "w") as f:
                json.dump(run_data, f, indent=4)

    def _get_func_str(self, func):
        return inspect.getsource(func)

    def _get_file_path(self, model_func):
        if not os.path.exists(self.date_path):
            os.makedirs(self.date_path)

        return self.model_path + self.meta_data_name

    def _collect(self, memory_dict):
        para_pd, metrics_pd = self._get_opt_meta_data(memory_dict)

        if para_pd is None:
            return None

        md_model = pd.concat([para_pd, metrics_pd], axis=1, ignore_index=False)

        return md_model

    def pos2para(self, pos):
        values_dict = {}
        for i, key in enumerate(self.search_space.keys()):
            pos_ = int(pos[i])
            values_dict[key] = list(self.search_space[key])[pos_]

        return values_dict

    def _get_opt_meta_data(self, memory_dict):
        results_dict = {}
        para_list = []
        score_list = []

        if not memory_dict:
            return None, None

        for key in memory_dict.keys():
            pos = np.fromstring(key, dtype=int)
            para = self.pos2para(pos)
            score = memory_dict[key]

            for key in para.keys():
                if (
                    not isinstance(para[key], int)
                    and not isinstance(para[key], float)
                    and not isinstance(para[key], str)
                ):

                    para_dill = dill.dumps(para[key])
                    para_hash = object_hash(para_dill)

                    with open(
                        self.model_path + str(para_hash) + ".pkl", "wb"
                    ) as pickle_file:
                        dill.dump(para_dill, pickle_file)

                    para[key] = para_hash

            if score != 0:
                para_list.append(para)
                score_list.append(score)

        results_dict["params"] = para_list
        results_dict["score"] = score_list

        return (
            pd.DataFrame(para_list),
            pd.DataFrame(score_list),
        )

    def _save_toCSV(self, meta_data_new, path):
        if os.path.exists(path):
            meta_data_old = pd.read_csv(path)

            assert len(meta_data_old.columns) == len(
                meta_data_new.columns
            ), "Warning meta data dimensionality does not match"

            meta_data = meta_data_old.append(meta_data_new)

            columns = list(meta_data.columns)
            noScore = ["_score_", "cv_default_score", "eval_time", "run"]
            columns_noScore = [c for c in columns if c not in noScore]

            meta_data = meta_data.drop_duplicates(subset=columns_noScore)
        else:
            meta_data = meta_data_new

        meta_data.to_csv(path, index=False)
