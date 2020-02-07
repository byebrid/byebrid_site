"""joe-rogan.py

Script to find those Joe "Insert funny reference here" Rogan comments on 
youtube.

"""
from googleapiclient.discovery import build
import googleapiclient.errors
import json
import re
import logging
import datetime
import pytz
import time
from django_project.settings import config


# The regex used to find comments with those dumb quotes
joe_rogan_re = re.compile('Joe .* Rogan', flags=re.I)

API_KEY = config.get("YOUTUBE_API_KEY")
service = build(serviceName='youtube', version='v3', developerKey=API_KEY)


def get_response(service_call, method, **kwargs):
    """Returns response from youtube service and handles API rate limit by 
    sleeping until API is available again.

    Example
    -------
    service.playlistItems().list(**kwargs) can be retrieved as 
    >>> get_response(service.playlistItems(), 'list', **kwargs)
    """
    f = getattr(service_call, method)

    try:
        return f(**kwargs).execute()
    except googleapiclient.errors.HttpError:
        # Getting duration of time until midnight (pacific time), which is when
        # API limit resets.
        pacific_tz = pytz.timezone('Canada/Pacific')
        now = datetime.datetime.now(pacific_tz)
        tomorrow = now + datetime.timedelta(days=1)
        midnight = datetime.datetime(tomorrow.year, tomorrow.month, tomorrow.day)
        # Need both datetimes to be aware to subtract them
        midnight = pacific_tz.localize(midnight)

        seconds_until_midnight = (midnight - now).seconds + 10 # A little leeway

        while True:
            time.sleep(600)
            if datetime.datetime.now(pacific_tz) > midnight:
                break
        # time.sleep(seconds_until_midnight)

        # Try the API call again
        return f(**kwargs).execute()
    except:
        raise


def get_comments(service, video_id):
    """Generator for comments on given youtube video.
    
    Parameters
    ----------
    service: youtube service
        As obtained from googleapiclient.discovery.build()
    video_id: str
    """
    response = get_response(service.commentThreads(), 'list',
        part='snippet', 
        textFormat='plainText',
        videoId=video_id,
        maxResults=100
    )

    # The return value
    comments = []
    while response:
        for item in response['items']:
            comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
            yield comment

        # If there are still more comments to retrieve, keep looping
        if 'nextPageToken' in response:
            page_token = response['nextPageToken']

            response = get_response(service.commentThreads(), 'list',
                part='snippet', 
                textFormat='plainText',
                videoId=video_id,
                maxResults=100,
                pageToken=page_token
            )
        else:
            break


def get_videos_from_playlist(service, playlist_id):
    """Generator of video ids from a given playlist."""
    response = get_response(service.playlistItems(), 'list',
        part='contentDetails',
        playlistId=playlist_id,
        maxResults=50
    )

    video_ids = []
    while response:
        for item in response['items']:
            video_id = item['contentDetails']['videoId']
            video_ids.append(video_id)
            yield video_id

        # If there are still more comments to retrieve, keep looping
        if 'nextPageToken' in response:
            page_token = response['nextPageToken']

            response = get_response(service.playlistItems(), 'list',
                part='contentDetails',
                playlistId=playlist_id,
                maxResults=50,
                pageToken=page_token
            )
        else:
            break

    return video_ids


def get_videos_from_channel(service, channel_id):
    """Generator of video ids from channel; returns channel's uploaded videos."""
    response = get_response(service.channels(), 'list',
        part='contentDetails',
        id=channel_id,
        maxResults=50
    )

    # Id for playlist of this channel's uploads
    uploads_id = response['items'][0]['contentDetails']['relatedPlaylists']['uploads']

    for video_id in get_videos_from_playlist(service=service, playlist_id=uploads_id):
        yield video_id


def joe_rogan_quote_generator():
    """Yields html list items containing joe rogan quotes from youtube comments"""
    yield 'Working on it...'
    yield 'Still working on it...'
    try:
        
        for video_id in get_videos_from_channel(service=service, channel_id='UCnxGkOGNMqQEUMvroOWps6Q'):
            for comment in get_comments(service=service, video_id=video_id):
                match = joe_rogan_re.match(comment)
                if match is not None:
                    yield f'<li>{match.group()}</li>'
    except:
        yield 'An error occurred!'


def main():
    joe_rogan_comments = []
    try:
        for video_id in get_videos_from_channel(service=service, channel_id='UCnxGkOGNMqQEUMvroOWps6Q'):
            for comment in get_comments(service=service, video_id=video_id):
                match = joe_rogan_re.match(comment)
                if match is not None:
                    joe_rogan_comments.append(match.group())
    except:
        pass

    return joe_rogan_comments


if __name__ == '__main__':
    main()
