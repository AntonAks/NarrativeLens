from newspaper import Article
from news_service.dtos.article import ArticleDTO


class Extractor:
    def extract_news_content(self, url: str) -> ArticleDTO:
        article = Article(url)
        article.download()
        article.parse()
        return ArticleDTO(
            title=article.title,
            text=article.text,
            authors=article.authors,
        )

