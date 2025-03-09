import json
import os

import requests
from typing import Any, Dict
from shared_tools.headline_analyzer import HeadlineAnalyzer
from shared_tools.s3_helper import S3Reader, S3Uploader


headlines_bucket_name = os.environ.get("HEADLINES_DATA_BUCKET", 'narrative-lens-headlines-data-dev')
upload_bucket_name = os.environ.get("RESULTS_DATA_BUCKET", 'narrative-lens-headlines-data-dev')

def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:

    result_dict = dict()

    analyzer = HeadlineAnalyzer(headlines_bucket_name)

    # Fetch headlines
    _titles = analyzer.get_headlines_from_s3()
    print("Titles:", _titles)

    # Extract top keywords
    keywords = analyzer.get_key_words(_titles)
    print("Top Keywords:", keywords)

if __name__ == '__main__':
    lambda_handler(None, None)

