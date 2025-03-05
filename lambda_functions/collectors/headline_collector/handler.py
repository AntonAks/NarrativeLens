import os
from typing import Any, Dict
from shared_tools.s3_helper import S3Reader, S3Uploader

bucket_data = os.environ.get("NEWS_DATA_BUCKET", 'news-analyzer-data-bucket')
bucket_headlines = os.environ.get("HEADLINES_DATA_BUCKET", 'headlines-analyzer-data-bucket')

def lambda_handler(event: Dict[str, Any], context: Any):

    headlines_collection = []

    reader = S3Reader(bucket_data)
    uploader = S3Uploader(bucket_headlines)
    date_prefix = uploader.get_date_prefix()
    for i in reader.list_files(date_prefix):
        headlines_collection.extend(reader.read_json(i))


    uploader.upload_json(
        data=headlines_collection,
        key_name='headlines'
    )
