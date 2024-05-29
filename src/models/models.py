# models.py
import faust

class ScrapedNews(faust.Record, serializer='json'):
    image_url: str
    title: str
    article_url: str
    summary: str
    category: str
    content: str
    author: str
    source: str
    published_date: str
