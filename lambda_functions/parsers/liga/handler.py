import json
import os

import requests
from bs4 import BeautifulSoup
from typing import Any, Dict
from shared_tools.s3_helper import S3Uploader

URL = "https://news.liga.net/ua"
PARSER_NAME = "liga"

bucket_name = os.environ.get("BUCKET_NAME")
s3_uploader = S3Uploader(bucket_name)

def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    try:
        _response = requests.get(URL)

        _list: list[dict[str, Any]] = []

        if _response.status_code == 200:
            html_content = _response.text
            soup = BeautifulSoup(html_content, 'html.parser')
            headlines = soup.find_all(class_='news-card news-list-page__card')

            for headline in headlines:
                a_tags = headline.find_all('a')
                for a_tag in a_tags:
                    if "https://" in a_tag.get('href') and len(str(a_tag.getText())) > 30:
                        _list.append(
                            {
                                "source": __name__,
                                "title": str(a_tag.getText()).strip(),
                                "url": str(a_tag.get('href')),
                            }
                        )

            s3_uploader.upload_json({"news": _list}, PARSER_NAME)

            return {
                'statusCode': 200,
                'body': json.dumps({
                    'message': 'News parsed successfully!',
                    'num_posts': len(_list),
                })
            }
        else:
            return {
                'statusCode': 500,
                'body': json.dumps({'message': 'Lambda error!'})
            }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'message': str(e)})
        }

if __name__ == '__main__':
    response = lambda_handler({}, None)
    print(response)