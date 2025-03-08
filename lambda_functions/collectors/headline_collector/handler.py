import os
from typing import Any, Dict
from shared_tools.s3_helper import S3Reader, S3Uploader

bucket_data = os.environ.get("NEWS_DATA_BUCKET", 'news-analyzer-data-bucket')
bucket_headlines = os.environ.get("HEADLINES_DATA_BUCKET", 'headlines-analyzer-data-bucket')

def lambda_handler(event: Dict[str, Any], context: Any):

    headlines_collection = []
    headlines_dict = {}

    reader = S3Reader(bucket_data)
    uploader = S3Uploader(bucket_headlines)
    date_prefix = uploader.get_date_prefix()
    for file in reader.list_files(date_prefix):
        headlines_collection.extend(reader.read_json(file))

    for headline in headlines_collection:
        headlines_dict[headline['title']] = headline

    print("Headlines collection:", headlines_dict)
    uploader.upload_json(
        data=headlines_dict,
        key_name='headlines'
    )
