import pytest
from src.quality_gate import check_quality


@pytest.mark.parametrize("f1", [0.0, 0.6499, float("nan"), float("inf"), 1.01])
def test_quality_gate_blocks_bad_models(f1):
    with pytest.raises(ValueError):
        check_quality(f1)


@pytest.mark.parametrize("f1", [0.65, 0.8, 1.0])
def test_quality_gate_accepts_threshold(f1):
    check_quality(f1)
