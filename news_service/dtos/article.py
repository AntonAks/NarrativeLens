from news_service.dtos.base import BaseDTO

class ArticleDTO(BaseDTO):
    title: str
    text: str
    authors: list[str] | None = None
