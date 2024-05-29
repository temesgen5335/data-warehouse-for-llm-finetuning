# models.py
import faust

class ScrapedData(faust.Record, serializer='json'):
    url: str
    title: str
    source: str

    def to_dict(self):
        return {
            'url': self.url,
            'title': self.title,
            'source': self.source,
        }