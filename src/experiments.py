"""Run three local experiments, select parameters, and export actual results."""
import json
from pathlib import Path
import yaml
from src.train import train


def main():
    settings = [
        {"n_estimators": 100, "learning_rate": 0.1, "max_depth": 3},
        {"n_estimators": 50, "learning_rate": 0.05, "max_depth": 2},
        {"n_estimators": 200, "learning_rate": 0.1, "max_depth": 5},
    ]
    results = []
    for params in settings:
        train(params)
        report = json.loads(Path("outputs/report.json").read_text())
        results.append({"params": params, **report})
    best = max(results, key=lambda item: item["f1_score"])
    Path("params.yaml").write_text(yaml.safe_dump(best["params"]), encoding="utf-8")
    train(best["params"])
    Path("outputs/experiments.json").write_text(
        json.dumps(results, indent=2), encoding="utf-8")
    print("Selected parameters:", best)


if __name__ == "__main__":
    main()
