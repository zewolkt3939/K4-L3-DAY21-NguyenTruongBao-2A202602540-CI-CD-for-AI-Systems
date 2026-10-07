"""Configure DVC locally so the committed config contains no credentials."""
import os
import subprocess


def main():
    bucket = os.environ["ARTIFACT_BUCKET"]
    subprocess.run(["dvc", "remote", "add", "--local", "-f", "-d",
                    "labstore", f"s3://{bucket}/dvc"], check=True)


if __name__ == "__main__":
    main()
