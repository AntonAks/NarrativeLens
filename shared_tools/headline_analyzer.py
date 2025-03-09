import json

import boto3
import nltk
from collections import Counter
from typing import List, Dict, Any
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from shared_tools.s3_helper import S3Reader

# Download necessary NLTK resources (run once)
nltk.download("punkt")
nltk.download("stopwords")
nltk.download('punkt_tab')

# Define stop words for filtering
stop_words = set(stopwords.words("english"))


class HeadlineAnalyzer:
    def __init__(self, bucket_name: str):
        self.bucket_name = bucket_name
        self.s3_reader = S3Reader(bucket_name)

    def get_headlines_from_s3(self) -> List[str]:
        """Fetches article headlines from S3."""
        prefix = self.s3_reader.get_date_prefix()
        json_data: dict[str, Any] = self.s3_reader.read_json(prefix + '/headlines.json')
        titles = list(json_data.keys())
        return titles

    def get_key_words(self, titles: List[str]) -> Dict[str, int]:
        """Processes headlines and returns the top 20 keywords with their frequency."""
        words = []
        for title in titles:
            tokens = word_tokenize(title.lower())  # Tokenization
            words.extend([word for word in tokens if word.isalpha() and word not in stop_words])  # Filtering

        word_counts = Counter(words)  # Count word occurrences
        return dict(word_counts.most_common(20))  # Return top 20 keywords


    def get_important_headlines(self, headlines, max_results=10) -> List[str]:
        bedrock_runtime = boto3.client(
            service_name='bedrock-runtime',
            region_name='us-east-1'
        )

        prompt = f"""
        Analyze the following news headlines and select the most important ones in terms of politics, economics, and security.
        For each category, provide up to {max_results} headlines ranked by importance.
        If a headline doesn't fit any category, ignore it.

        Headlines:
        {json.dumps(headlines)}

        Output should be in JSON format with the following structure:
        {{
            "politics": [
                {{
                    "headline": "Headline text",
                    "importance_score": 8.5,
                    "reasoning": "Brief explanation of why this is politically important"
                }}
            ],
            "economics": [...],
            "security": [...]
        }}

        Each category should have headlines sorted by importance_score in descending order.
        Only include headlines that are truly relevant to each category.
        """

        model_id = "meta.llama3-8b-instruct-v1:0"

        response = bedrock_runtime.invoke_model(
            modelId=model_id,
            contentType="application/json",
            accept="application/json",
            body=json.dumps({
                "prompt": prompt,
                "max_gen_len": 2000,
                "temperature": 0.3,
                "top_p": 0.9
            })
        )

        print(">>>>>>>>>>>>>>>>")
        response_body = json.loads(response.get('body').read())
        print(">>>", response_body)
        print(">>>>>>>>>>>>>>>>")


        result = json.loads(response_body.get('completion'))

        return result

if __name__ == "__main__":
    analyzer = HeadlineAnalyzer("narrative-lens-headlines-data-dev")

    # Fetch headlines
    _titles = analyzer.get_headlines_from_s3()
    print("Titles:", _titles)

    # Extract top keywords
    keywords = analyzer.get_key_words(_titles)
    print("Top Keywords:", keywords)


    important_headlines = analyzer.get_important_headlines(_titles)
    print(important_headlines)