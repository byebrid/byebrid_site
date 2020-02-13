from django.db import models
import json


class JoeRoganPost(models.Model):
    video_id = models.CharField(max_length=32, unique=True)
    title = models.CharField(max_length=64)
    thumbnail_url = models.CharField(max_length=64)
    # THIS EXPECTS A JSON-FORMATTED STRING!
    _quotes = models.CharField(max_length=8192, default='[]')

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    posts = models.Manager()

    @property
    def url(self):
        return f'https://www.youtube.com/watch?v={self.video_id}'

    @property
    def quotes(self):
        quotes = json.loads(self._quotes)
        return [quote for quote in sorted(quotes, key=lambda quote: quote['like_count'] + quote['replies'], reverse=True)]

    def __str__(self):
        return f'{self.video_id}: {self.title}'
