import boto3
import datetime
import json
from typing import Any


class S3Uploader:
    def __init__(self, bucket_name: str):
        self.s3 = boto3.client("s3")
        self.bucket_name = bucket_name

    def _get_date_prefix(self) -> str:
        return datetime.datetime.now().strftime("%Y/%m/%d")

    def upload_json(self, data: Any, key_name: str):
        date_prefix = self._get_date_prefix()
        s3_key = f"{date_prefix}/{key_name}.json"

        json_data = json.dumps(data, ensure_ascii=False, indent=4)
        self.s3.put_object(
            Bucket=self.bucket_name,
            Key=s3_key,
            Body=json_data,
            ContentType="application/json",
        )

        return f"s3://{self.bucket_name}/{s3_key}"

    def upload_text(self, text: str, key_name: str):
        date_prefix = self._get_date_prefix()
        s3_key = f"{date_prefix}/{key_name}.txt"

        self.s3.put_object(
            Bucket=self.bucket_name,
            Key=s3_key,
            Body=text,
            ContentType="text/plain",
        )

        return f"s3://{self.bucket_name}/{s3_key}"
