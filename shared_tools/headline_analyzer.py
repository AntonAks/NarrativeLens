import json

import boto3
import nltk
from collections import Counter
from typing import List, Dict, Any

from newspaper import Article
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
    def __init__(self, bucket_name: str, region: str):
        self.bucket_name = bucket_name
        self.s3_reader = S3Reader(bucket_name)
        self.headlines: dict[str, Any] = self.s3_reader.read_json(self.s3_reader.get_date_prefix() + '/headlines.json')
        self.model_id = "amazon.nova-lite-v1:0"

        self.bedrock_runtime = boto3.client(
            service_name='bedrock-runtime',
            region_name=region
        )

    def get_headlines_from_s3(self) -> List[str]:
        return list(self.headlines.keys())

    def get_key_words(self, titles: List[str]) -> Dict[str, int]:
        """Processes headlines and returns the top 20 keywords with their frequency."""
        words = []
        for title in titles:
            tokens = word_tokenize(title.lower())  # Tokenization
            words.extend([word for word in tokens if word.isalpha() and word not in stop_words])  # Filtering

        word_counts = Counter(words)  # Count word occurrences
        return dict(word_counts.most_common(20))  # Return top 20 keywords

    def get_important_headlines(self, max_results=10) -> List[str]:
        prompt = f"""
                Your task is to analyze the given news headlines and select the {max_results} most important ones, based on relevance to politics, economy, and security.
                Instructions: Consider the global impact, policy implications, financial consequences, and security concerns. 
                **Return ONLY a JSON list** with the selected headlines. 
                Do **not** include any explanations, code, or additional text.
                Headlines: {list(self.headlines.keys())}
        """

        # Send the message to the model, using a basic inference configuration.
        response = self.bedrock_runtime.converse(
            modelId=self.model_id,
            messages=[
                {
                    "role": "user",
                    "content": [{"text": prompt}],
                }
            ],
            inferenceConfig={"maxTokens": 512, "temperature": 0.5, "topP": 0.9},
        )

        # Extract and print the response text.
        response_text = response["output"]["message"]["content"][0]["text"]
        return response_text

    def get_summary_by_title(self, title: str) -> str:
        url = self.headlines[title]['url']

        article = Article(url)
        article.download()
        article.parse()

        prompt = f"""
                Your task is to analyze the given article and provide a detailed summary of it with key points. 
                Without formating.
                Title: {title}
                Text: {article.text}
                
                Example of the output:
                ### Summary of the (article title)
                1. Key point name:
                   - ...
                   - ...
                
                2. Key point name:
                   - ...
        """

        # Send the message to the model, using a basic inference configuration.
        response = self.bedrock_runtime.converse(
            modelId=self.model_id,
            messages=[
                {
                    "role": "user",
                    "content": [{"text": prompt}],
                }
            ],
            inferenceConfig={"maxTokens": 512, "temperature": 0.5, "topP": 0.9},
        )

        # Extract and print the response text.
        response_text = response["output"]["message"]["content"][0]["text"]
        return response_text


if __name__ == "__main__":
    analyzer = HeadlineAnalyzer("narrative-lens-headlines-data-dev", "us-east-1")

    # # Fetch headlines
    # _titles = analyzer.get_headlines_from_s3()
    # print("Titles:", _titles)
    #
    # # Extract top keywords
    # keywords = analyzer.get_key_words(_titles)
    # print("Top Keywords:", keywords)
    #
    important_headlines = analyzer.get_important_headlines(5)
    print(important_headlines)

    response = analyzer.get_summary_by_title('Speaker Johnson unveils bill to fund the government through September 30')
    print(">>>>", response.strip())