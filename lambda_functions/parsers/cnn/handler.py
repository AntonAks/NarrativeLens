import json
import os

import requests
from bs4 import BeautifulSoup
from typing import Any, Dict
from shared_tools.s3_helper import S3Uploader

URL = "https://edition.cnn.com/politics"
PARSER_NAME = "cnn_politics"

bucket_name = os.environ.get("NEWS_DATA_BUCKET", 'news-analyzer-data-bucket')
s3_uploader = S3Uploader(bucket_name)


def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    _response = requests.get(URL)

    _list: list[dict[str, Any]] = []

    if _response.status_code == 200:
        html_content = _response.text
        soup = BeautifulSoup(html_content, 'html.parser')
        articles = soup.find_all(
            class_='container__link container__link--type-article container_lead-plus-headlines__link')

        for article in articles:
            href = article.get('href')
            headline = article.find_all(class_='container__headline-text')
            if len(headline) > 0:
                _list.append(
                    {
                        "source": PARSER_NAME,
                        "title": headline[0].text,
                        "url": 'https://edition.cnn.com' + href,
                    }
                )

        file_path = s3_uploader.upload_json(
            data=_list,
            key_name=PARSER_NAME
        )

        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'News parsed successfully!',
                'num_posts': len(_list),
                'file_path': file_path
            })
        }
