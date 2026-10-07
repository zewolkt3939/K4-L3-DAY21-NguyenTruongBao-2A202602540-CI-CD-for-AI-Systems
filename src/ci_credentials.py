"""Write cloud credentials to GitHub's environment file without logging secrets."""
import json
import os


def main():
    credentials = json.loads(os.environ["STORAGE_CREDENTIALS"])
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
