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


if __name__ == "__main__":
    analyzer = HeadlineAnalyzer("narrative-lens-headlines-data-dev")

    # Fetch headlines
    _titles = analyzer.get_headlines_from_s3()
    print("Titles:", _titles)

    # Extract top keywords
    keywords = analyzer.get_key_words(_titles)
    print("Top Keywords:", keywords)
