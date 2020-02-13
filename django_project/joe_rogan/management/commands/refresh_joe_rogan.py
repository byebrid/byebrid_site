"""
Management script to update database of 'Joe <Insert quote here> Rogan' 
comments from videos on the 'JRE Clips' youtube channel.

This can be run simply with:
```
python manage.py refresh_joe_rogan
```

NOTE: Not sure if it would be better to place functions as methods in Command
class or if I should just leave them out. Doesn't really affect functionality 
but something to ponder (actually uses self.stdout.write so does slightly 
affect functionality).
"""
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from joe_rogan.models import JoeRoganPost
import json
import os

# From the original joe-rogan.py file, minus already-imported modules
from googleapiclient.discovery import build
import googleapiclient.errors
import re
import logging
import datetime
import pytz
import time


BASE_DIR = settings.BASE_DIR
# Getting API key and building youtube api service
with open(os.path.join(BASE_DIR, 'config.json'), 'r') as f:
    config = json.load(f)

API_KEYS = config.get('YOUTUBE_API_KEYS')


class OutOfQuota(Exception):
    pass
    

class Command(BaseCommand):
    help = 'Refreshes the database of Joe Rogan posts based off of the json file.'

    current_api_key = None

    def add_arguments(self, parser):
        parser.add_argument('--overwrite', action='store_true',
            help='Recommended to not use this. If this option is provided, videos will NOT be skipped over if they are already in the database (poor use of API quota).'
        )
        
    def handle(self, *args, **options):
        """The meat and bones of the management command. Where the API is 
        actually called upon and where comments are filtered out. Also adds the
        results to the database.
        """
        self.service = self.build_service()
        # The regex used to find comments with those quotes
        joe_rogan_re = re.compile('Joe .* Rogan', flags=re.I)

        # The ``channel_id`` corrseponds to JRE Clips youtube channel
        for i, video in enumerate(self.get_videos_from_channel(channel_id='UCnxGkOGNMqQEUMvroOWps6Q')):
            video_id = video['video_id']

            if not options['overwrite']:
                model_already_created = JoeRoganPost.posts.filter(video_id=video_id)
                # Not sending any more requests if we already have this video in database
                if model_already_created and model_already_created[0] != JoeRoganPost.posts.last():
                    continue
                    
            title = video['title']
            thumbnail = video['thumbnail']
            video_dict = {
                'title': title,
                'video_id': video_id,
                'thumbnail': thumbnail,
                'quotes': []
            }
            # Filtering those Joe Rogan comments from all comments on video
            for comment in self.get_comments(video_id=video_id):
                match = joe_rogan_re.match(comment['text'])
                if match is not None:
                    comment['text'] = match.group()
                    video_dict['quotes'].append(comment)

            self.create_model(video_dict=video_dict)
    
    def get_comments(self, video_id):
        """Generator for comments on given youtube video.
        
        Yields
        ------
        comment: dict
            ...

        Parameters
        ----------
        video_id: str
            I.e. the `v` parameter in a youtube video's url.
        """
        response = self.get_response(methods=['commentThreads', 'list'], 
            part='snippet', 
            textFormat='html',
            videoId=video_id,
            maxResults=100
        )

        while response:
            for item in response['items']:
                text = item['snippet']['topLevelComment']['snippet']['textDisplay']
                like_count = item['snippet']['topLevelComment']['snippet']['likeCount']
                replies = item['snippet']['totalReplyCount']
                yield {
                    'text': text,
                    'like_count': like_count,
                    'replies': replies
                }

            if 'nextPageToken' in response:
                page_token = response['nextPageToken']

                response = self.get_response(methods=['commentThreads', 'list'], 
                    part='snippet', 
                    textFormat='html',
                    videoId=video_id,
                    maxResults=100,
                    pageToken=page_token
                )
            else:
                break

    def get_videos_from_channel(self, channel_id):
        """Essentially a wrapper (but not really) for get_videos_from_playlist()

        See get_videos_from_playlist() to see return values.
        
        Parameters
        ----------
        channel_id: str
            Can be found in the url of a youtube channel's page.
        """
        response = self.get_response(methods=['channels', 'list'],
            part='contentDetails',
            id=channel_id,
            maxResults=50
        )

        # Id for playlist of this channel's uploads
        uploads_id = response['items'][0]['contentDetails']['relatedPlaylists']['uploads']

        for video in self.get_videos_from_playlist(playlist_id=uploads_id):
            yield video

    def get_videos_from_playlist(self, playlist_id):
        """Generates videos from a given playlist.

        This is used in get_videos_from_channel() to find all videos uploaded by a 
        given channel.
        
        Yields 
        ------
        {
            'video_id': <video's id>, 
            'title': <video's title>,
            'thumbnail': <video's maximum resolution thumbnail>
        }
        
        Parameters
        ----------
        playlist_id: str
            Can be found in the url of a youtube playlist.
        """
        response = self.get_response(methods=['playlistItems', 'list'],
            part='snippet',
            playlistId=playlist_id,
            maxResults=50
        )

        while response:
            for item in response['items']:
                video_id = item['snippet']['resourceId']['videoId']
                title = item['snippet']['title']
                # Getting best resoultion thumbnail
                for resolution in ['maxres', 'high', 'medium', 'default']:
                    if resolution in item['snippet']['thumbnails']:
                        thumbnail = item['snippet']['thumbnails'][resolution]['url']
                        break

                yield {
                    'video_id': video_id,
                    'title': title,
                    'thumbnail': thumbnail
                }
                
            if 'nextPageToken' in response:
                page_token = response['nextPageToken']

                response = self.get_response(methods=['playlistItems', 'list'],
                    part='contentDetails,snippet',
                    playlistId=playlist_id,
                    maxResults=50,
                    pageToken=page_token
                )
            else:
                break

    def create_model(self, video_dict):
        """Creates new model from video or, if video already in database, 
        simply updates the `quotes` field in the database.
        """
        quotes = video_dict['quotes']
        if len(quotes) == 0:
            return
            
        quotes_str = json.dumps(quotes) # For CharField in model
        thumbnail = video_dict['thumbnail']
        title = video_dict['title']
        video_id = video_dict['video_id']

        model_already_created = JoeRoganPost.posts.filter(video_id=video_id)
        if model_already_created:
            model_already_created.update(_quotes=quotes_str)
            self.stdout.write(self.style.SUCCESS(f"Succesfully updated quotes from video {video_id}"))
        else:
            JoeRoganPost.posts.create(
                video_id=video_id,
                title=title,
                thumbnail_url=thumbnail,
                _quotes=quotes_str
            )
            self.stdout.write(self.style.SUCCESS(f"Succesfully created Joe Rogan post from video {video_id}"))

    def get_response(self, methods, **kwargs):
        """Returns response from youtube service and handles API rate limit by 
        sleeping until API is available again.

        Example
        -------
        service.playlistItems().list(**kwargs) can be retrieved as 
        >>> get_response(methods=['playlistItems', 'list'], **kwargs)

        Parameters
        ----------
        methods: iterable of strs
            Names of methods to call on service. Last method in iterable gets 
            called with ``kwargs``.
        kwargs: .
        """
        def get_request():
            """Uses given ``methods`` to get a request object which we can 
            execute to get a response."""
            # self.stdout.write(f'Getting request from methods = {methods}')
            request = self.service
            for method in methods[:-1]:
                request = getattr(request, method)
                request = request() # Call that last method

            request = getattr(request, methods[-1])
            return request(**kwargs)

        try:
            request = get_request()
            response = request.execute()
            return response
        except googleapiclient.errors.HttpError as err:
            self.stdout.write(self.style.NOTICE(err))
            # NOTE: Add if statement here to check if error has key phrase in it (i.e. 'exceeded api quota')
            try:
                self.service = self.build_service()
                request = get_request()
                response = request.execute()
                self.stdout.write('Succesfully cycled API keys...')
                return response
            except OutOfQuota:       
                self.stdout.write(self.style.NOTICE('Sleeping until midnight pacific time since we reached quota limit...'))
                # Getting duration of time until midnight (pacific time), which is when
                # API limit resets.
                pacific_tz = pytz.timezone('Canada/Pacific')
                now = datetime.datetime.now(pacific_tz)
                tomorrow = now + datetime.timedelta(days=1)
                # NOTE: Actually adds 10 minutes to midnight as precaution
                midnight = datetime.datetime(tomorrow.year, tomorrow.month, tomorrow.day, 0, 10)
                # Need both datetimes to be aware to subtract them
                midnight = pacific_tz.localize(midnight)

                seconds_until_midnight = (midnight - now).seconds

                while True:
                    time.sleep(600)
                    if datetime.datetime.now(pacific_tz) > midnight:
                        break

                # Reset back to first API key and try again
                self.stdout.write('Now past midnight. Attempting to resume operation...')
                self.current_api_key = None
                self.service = self.build_service()
                request = get_request()
                response = request.execute()
                return response

    def build_service(self):
        """Builds youtube api service. Cycles through API keys until we've 
        actually run out of quota, at which point raises an `OutOfQuota`."""
        self.stdout.write('Building youtube api service...')
        if self.current_api_key is None:
            self.current_api_key = API_KEYS[0]
        else:
            current_index = API_KEYS.index(self.current_api_key)
            new_index = current_index + 1
            if new_index == len(API_KEYS):
                raise OutOfQuota
            else:
                self.current_api_key = API_KEYS[new_index]

        return build(serviceName='youtube', version='v3', developerKey=self.current_api_key)