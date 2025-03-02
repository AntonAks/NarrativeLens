import boto3
import io
import json
from datetime import datetime, timezone
from typing import Any


class S3Helper:
    def __init__(self, bucket_name: str):
        self.s3 = boto3.client("s3")
        self.bucket_name = bucket_name

    def get_date_prefix(self) -> str:
        return datetime.now(timezone.utc).strftime("%Y%m%d")


class S3Uploader(S3Helper):

    def upload_json(self, data: Any, key_name: str):
        date_prefix = self.get_date_prefix()
        s3_key = f"{date_prefix}/{key_name}.json"
        json_data = json.dumps(data, ensure_ascii=False, indent=4)
        self.s3.put_object(
            Bucket=self.bucket_name,
            Key=s3_key,
            Body=json_data,
            ContentType="application/json"
        )

        return f"s3://{self.bucket_name}/{s3_key}"

    def upload_text(self, text: str, key_name: str) -> str:
        date_prefix = self.get_date_prefix()
        s3_key = f"{date_prefix}/{key_name}.txt"

        self.s3.put_object(
            Bucket=self.bucket_name,
            Key=s3_key,
            Body=text,
            ContentType="text/plain",
        )

        return f"s3://{self.bucket_name}/{s3_key}"


class S3Reader(S3Helper):

    def list_files(self, prefix: str = "") -> list[str]:
        """Lists all files in the S3 bucket with an optional prefix."""
        response = self.s3.list_objects_v2(Bucket=self.bucket_name, Prefix=prefix)
        return [obj["Key"] for obj in response.get("Contents", [])]

    def read_json(self, file_key: str) -> dict[str, Any]:
        """Reads a JSON file from S3 and returns it as a Python dictionary."""
        response = self.s3.get_object(Bucket=self.bucket_name, Key=file_key)
        json_data = json.load(io.BytesIO(response["Body"].read()))
        return json_data


if __name__ == '__main__':
    reader = S3Reader("news-analyzer-data-bucket")

    for i in reader.list_files('20250302'):
        result = reader.read_json(i)
        print(result)
