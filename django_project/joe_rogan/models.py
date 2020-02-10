from django.db import models
from django.contrib.postgres.fields import ArrayField
import json

# Create your models here.

class JoeRoganPost(models.Model):
    video_id = models.CharField(max_length=32)
    title = models.CharField(max_length=64)
    thumbnail_url = models.CharField(max_length=64)
    # THIS EXPECTS A JSON-FORMATTED STRING!
    _quotes = models.CharField(max_length=2048, default='[]')
    posts = models.Manager()

    @property
    def url(self):
        return f'https://www.youtube.com/watch?v={self.video_id}'

    @property
    def quotes(self):
        return json.loads(self._quotes)

    def __str__(self):
        return f'{self.video_id}: {self.title}'
