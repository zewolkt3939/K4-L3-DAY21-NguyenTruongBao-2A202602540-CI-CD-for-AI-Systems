"""Write cloud credentials to GitHub's environment file without logging secrets."""
import json
import os


def _load_credentials():
    raw = os.getenv("STORAGE_CREDENTIALS", "").strip()
    if raw:
        try:
            credentials = json.loads(raw)
        except json.JSONDecodeError as exc:
            raise ValueError("STORAGE_CREDENTIALS must be valid JSON.") from exc
    else:
        credentials = {
            "aws_access_key_id": os.getenv("AWS_ACCESS_KEY_ID", ""),
            "aws_secret_access_key": os.getenv("AWS_SECRET_ACCESS_KEY", ""),
            "aws_session_token": os.getenv("AWS_SESSION_TOKEN", ""),
        }
    missing = [key for key in ("aws_access_key_id", "aws_secret_access_key")
               if not credentials.get(key)]
    if missing:
        raise ValueError("Missing AWS credentials. Set STORAGE_CREDENTIALS or "
                         "AWS_ACCESS_KEY_ID/AWS_SECRET_ACCESS_KEY.")
    return credentials


def main():
    credentials = _load_credentials()
    values = {
        "AWS_ACCESS_KEY_ID": credentials["aws_access_key_id"],
        "AWS_SECRET_ACCESS_KEY": credentials["aws_secret_access_key"],
    }
    if credentials.get("aws_session_token"):
        values["AWS_SESSION_TOKEN"] = credentials["aws_session_token"]
    with open(os.environ["GITHUB_ENV"], "a", encoding="utf-8") as stream:
        for key, value in values.items():
            if not value or "\n" in value or "\r" in value:
                raise ValueError(f"Invalid value for {key}")
            print(f"::add-mask::{value}")
            stream.write(f"{key}={value}\n")


if __name__ == "__main__":
    main()
