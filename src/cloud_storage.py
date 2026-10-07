"""Cloud model transfers. SDK credentials come from environment or VM identity."""
import argparse
import os
from pathlib import Path


def transfer(direction: str, bucket: str, key: str, filename: str):
    if direction == "download":
        Path(filename).parent.mkdir(parents=True, exist_ok=True)
    if direction in ("upload", "download"):
        import boto3
        client = boto3.client("s3")
        if direction == "download":
            client.download_file(bucket, key, filename)
        else:
            client.upload_file(filename, bucket, key)
    else:
        raise ValueError("direction must be upload or download")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("direction", choices=["upload", "download"])
    parser.add_argument("filename")
    parser.add_argument("key")
    args = parser.parse_args()
    transfer(args.direction, os.environ["ARTIFACT_BUCKET"], args.key, args.filename)


if __name__ == "__main__":
    main()
