import json
import os
import nltk
from collections import Counter
from typing import List, Dict
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from shared_tools.s3_helper import S3Uploader, S3Downloader

# Download necessary NLTK resources (run once)
nltk.download("punkt")
nltk.download("stopwords")

# Define stop words for filtering
stop_words = set(stopwords.words("english"))

class HeadlineAnalyzer:
    def __init__(self, bucket_name: str):
        self.bucket_name = bucket_name
        self.s3_downloader = S3Downloader(bucket_name)

    def get_titles_from_s3(self, parser_name: str) -> List[str]:
        """Fetches article headlines from S3."""
        json_data = self.s3_downloader.download_json(parser_name)
        return [item["title"] for item in json_data.get("news", [])]

    def process_titles(self, titles: List[str]) -> Dict[str, int]:
        """Processes headlines and returns the top 20 keywords with their frequency."""
        words = []
        for title in titles:
            tokens = word_tokenize(title.lower())  # Tokenization
            words.extend([word for word in tokens if word.isalpha() and word not in stop_words])  # Filtering

        word_counts = Counter(words)  # Count word occurrences
        return dict(word_counts.most_common(20))  # Return top 20 keywords

if __name__ == "__main__":
    bucket_name = os.getenv("BUCKET_NAME", "your-s3-bucket-name")
    analyzer = HeadlineAnalyzer(bucket_name)

    # Fetch headlines
    titles = analyzer.get_titles_from_s3("liga")
    print("Titles:", titles)

    # Extract top keywords
    keywords = analyzer.process_titles(titles)
    print("Top Keywords:", keywords)
