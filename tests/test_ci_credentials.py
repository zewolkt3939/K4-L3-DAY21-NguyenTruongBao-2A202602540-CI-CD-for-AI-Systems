import json

import pytest

from src import ci_credentials


def test_ci_credentials_reads_storage_credentials(tmp_path, monkeypatch):
    env_file = tmp_path / "github.env"
    monkeypatch.setenv("GITHUB_ENV", str(env_file))
    monkeypatch.setenv("STORAGE_CREDENTIALS", json.dumps({
        "aws_access_key_id": "key",
        "aws_secret_access_key": "secret",
    }))
    monkeypatch.delenv("AWS_ACCESS_KEY_ID", raising=False)
    monkeypatch.delenv("AWS_SECRET_ACCESS_KEY", raising=False)
    ci_credentials.main()
    content = env_file.read_text()
    assert "AWS_ACCESS_KEY_ID=key\n" in content
    assert "AWS_SECRET_ACCESS_KEY=secret\n" in content


def test_ci_credentials_falls_back_to_aws_env(tmp_path, monkeypatch):
    env_file = tmp_path / "github.env"
    monkeypatch.setenv("GITHUB_ENV", str(env_file))
    monkeypatch.setenv("STORAGE_CREDENTIALS", "")
    monkeypatch.setenv("AWS_ACCESS_KEY_ID", "key")
    monkeypatch.setenv("AWS_SECRET_ACCESS_KEY", "secret")
    monkeypatch.setenv("AWS_SESSION_TOKEN", "token")
    ci_credentials.main()
    content = env_file.read_text()
    assert "AWS_ACCESS_KEY_ID=key\n" in content
    assert "AWS_SECRET_ACCESS_KEY=secret\n" in content
    assert "AWS_SESSION_TOKEN=token\n" in content


def test_ci_credentials_requires_credentials(tmp_path, monkeypatch):
    monkeypatch.setenv("GITHUB_ENV", str(tmp_path / "github.env"))
    monkeypatch.setenv("STORAGE_CREDENTIALS", "")
    monkeypatch.delenv("AWS_ACCESS_KEY_ID", raising=False)
    monkeypatch.delenv("AWS_SECRET_ACCESS_KEY", raising=False)
    with pytest.raises(ValueError, match="Missing AWS credentials"):
        ci_credentials.main()
