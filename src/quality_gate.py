import math
import os


def check_quality(f1: float, threshold: float = 0.65):
    if not math.isfinite(f1) or not threshold <= f1 <= 1:
        raise ValueError(f"FAILED: f1_score {f1} must be within [{threshold}, 1].")
    print(f"PASSED: f1_score {f1:.4f} >= {threshold:.2f}")


def main():
    check_quality(float(os.environ["MODEL_F1"]))


if __name__ == "__main__":
    main()
