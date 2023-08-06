from itertools import islice
import numpy as np
import pandas as pd

import jf.sklearn_import


class ColumnSelector:
    def __init__(self, column, default=["unk"]):
        self.column = column
        self.default = default

    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None):
        if isinstance(X, (tuple, list)):
            X = pd.DataFrame(X)
        # Add selected columns to dataframe if needed
        if isinstance(self.column, (tuple, list)):
            for col in self.column:
                if col not in X.columns:
                    X[col] = "unk"
        else:
            if self.column not in X.columns:
                X[self.column] = "unk"
        return X[self.column]


class transform(jf.process.JFTransformation):
    def _fn(self, arr):
        params = self.args[0]
        model = params

        print(model)

        y = None
        data = list(zip(*list(arr)))
        if len(data) == 2:
            data, y = data
        try:
            yield from np.array(model.fit_transform(data).todense())
        except:
            yield from np.array(model.fit_transform(data))


class trainer(jf.process.JFTransformation):
    def _fn(self, arr):
        params = self.args[0]
        model = params

        y = None
        data = list(zip(*list(arr)))
        if len(data) == 2:
            data, y = data
        print(f"Training the model ({model}):")
        model.fit(data, y)

        yield model


class persistent_trainer(jf.process.JFTransformation):
    def _fn(self, arr):
        import pickle

        params = self.args
        ofn, model = params
        ofn = ofn.replace("__JFESCAPED__", "")

        model = next(trainer(model).transform(arr))

        print(f"Saving model to {ofn}")
        with open(ofn, "wb") as f:
            f.write(pickle.dumps(model))
        yield model


class persistent_transformation(jf.process.JFTransformation):
    def _fn(self, arr):
        import pickle

        params = self.args
        ofn, model = params
        ofn = ofn.replace("__JFESCAPED__", "")

        print(model)
        print(list(model.transform([{"status": 1}])))

        with open(ofn, "wb") as f:
            f.write(pickle.dumps(model))
        yield model


class importResolver:
    def __getattribute__(self, k):
        k = k.replace("__JFESCAPED__", "")
        if k == "persistent_transformation":
            return persistent_transformation
        if k == "persistent_trainer":
            return persistent_trainer
        if k == "print":
            return Print
        if k == "trainer":
            return trainer
        if k == "transform":
            return transform
        if k == "ColumnSelector":
            return ColumnSelector
        else:
            mod = jf.sklearn_import.import_from_sklearn(k)
            if mod is not None:
                return mod
        print(f"Failed to import {k}")


import_resolver = importResolver()
