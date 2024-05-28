# models.py
import faust

class ScrapedNews(faust.Record, serializer='json'):
    image_url: str
    title: str
    article_url: str
    category: str
    author: str
    summary: str
    content: str
    source: str
    published_date: str