# models.py
import faust

class ScrapedData(faust.Record, serializer='json'):
  url: str
  title: str
  source: str