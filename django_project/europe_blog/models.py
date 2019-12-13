from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from ckeditor_uploader.fields import RichTextUploadingField


# Create your models here.
class EuropePost(models.Model):
    location = models.CharField(max_length=100)
    arrival_date = models.DateField()
    departure_date = models.DateField()
    content = RichTextUploadingField()
    date_posted = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.location}: {self.arrival_date}'

    def get_absolute_url(self):
        return reverse('europe_post_detail', kwargs={'pk': self.pk})