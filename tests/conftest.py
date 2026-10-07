import numpy as np
import pandas as pd
import pytest

from src.train import FEATURE_NAMES, train


@pytest.fixture
def trained(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    monkeypatch.setenv("MLFLOW_TRACKING_URI", f"sqlite:///{tmp_path / 'mlflow.db'}")
    rng = np.random.default_rng(0)
    frame = pd.DataFrame(rng.random((200, len(FEATURE_NAMES))), columns=FEATURE_NAMES)
    frame["target"] = rng.integers(0, 2, size=200)
    frame.iloc[:160].to_csv("train.csv", index=False)
    frame.iloc[160:].to_csv("holdout.csv", index=False)
    return train({"n_estimators": 10, "learning_rate": 0.1, "max_depth": 2},
                 "train.csv", "holdout.csv")


