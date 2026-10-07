import json
from pathlib import Path
import joblib
import pandas as pd
from sklearn.metrics import f1_score
from src.train import FEATURE_NAMES


def test_train_returns_float(trained):
    assert isinstance(trained, float)
    assert 0 <= trained <= 1


def test_report_file_created(trained):
    report = json.loads(Path("outputs/report.json").read_text())
    assert report["f1_score"] == trained
    assert 0 <= report["accuracy"] <= 1
    model = joblib.load("models/model.joblib")
    holdout = pd.read_csv("holdout.csv")
    expected = f1_score(holdout["target"], model.predict(holdout[FEATURE_NAMES]))
    assert report["f1_score"] == expected


def test_model_file_created(trained):
    model = joblib.load("models/model.joblib")
    assert model.n_features_in_ == 10
    assert set(model.classes_) == {0, 1}
