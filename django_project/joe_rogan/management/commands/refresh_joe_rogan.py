"""Script to check joe_rogan.json file and convert that into Joe Rogan Posts
which can be stored in the database.
"""
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from joe_rogan.models import JoeRoganPost
import json
import os
import inspect


BASE_DIR = settings.BASE_DIR


class Command(BaseCommand):
    help = 'Refreshes the database of Joe Rogan posts based off of the json file.'

    def handle(self, *args, **options):
        filepath = os.path.join(BASE_DIR, 'joe_rogan', 'joe_rogan.json')
        with open(filepath, 'r') as f:
            joe_rogan_posts = json.load(f)

        JoeRoganPost.posts.all().delete()

        for title, post in joe_rogan_posts.items():
            quotes = post['quotes']
            if len(quotes) == 0:
                continue

            quotes_str = json.dumps(quotes)
            JoeRoganPost.posts.create(
                video_id=post['id'],
                title=title,
                thumbnail_url=post['thumbnail']['url'],
                _quotes=quotes_str
            )
            self.stdout.write(self.style.SUCCESS(f"Succesfully created Joe Rogan post from video {post['id']}"))