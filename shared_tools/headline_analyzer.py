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

        model_id = "amazon.nova-lite-v1:0"

        prompt = f"""
                Your task is to analyze the given news headlines and select the {max_results} most important ones, based on relevance to politics, economy, and security.
                Instructions: Consider the global impact, policy implications, financial consequences, and security concerns. 
                **Return ONLY a JSON list** with the selected headlines. 
                Do **not** include any explanations, code, or additional text.
                Headlines: {headlines}
        """
        # Start a conversation with the user message.
        user_message = "Describe the purpose of a 'hello world' program in one line."
        conversation = [
            {
                "role": "user",
                "content": [{"text": prompt}],
            }
        ]

        # Send the message to the model, using a basic inference configuration.
        response = bedrock_runtime.converse(
            modelId=model_id,
            messages=conversation,
            inferenceConfig={"maxTokens": 512, "temperature": 0.5, "topP": 0.9},
        )

        # Extract and print the response text.
        response_text = response["output"]["message"]["content"][0]["text"]
        print(response_text)


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
