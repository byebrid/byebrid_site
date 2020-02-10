from django.shortcuts import render
from django.conf import settings
from django.core.paginator import Paginator
import os
import datetime
import pytz
import json

BASE_DIR = settings.BASE_DIR


def home(request):
    filepath = os.path.join(BASE_DIR, 'joe_rogan', 'joe_rogan.json')
    with open(filepath, 'r') as f:
        videos = json.load(f)

    for title in list(videos.keys()):
        if len(videos[title]['quotes']) == 0:
            videos.pop(title)
        else:
            id = videos[title]['id']
            url = f'https://www.youtube.com/watch?v={id}'
            videos[title]['url'] = url

    last_updated_time = os.path.getmtime(filepath)
    tz = pytz.timezone('Australia/Melbourne')
    last_updated_date = datetime.datetime.fromtimestamp(last_updated_time, tz)
    last_updated_display = last_updated_date.strftime('%a %-d %b, %Y')

    # paginator = Paginator(quotes, 50)
    # page_number = request.GET.get('page')
    # page_obj = paginator.get_page(page_number)

    context = {
        'title': "Joe \"Joe Rogan\" Rogan",
        'videos': videos,
        # 'page_obj': page_obj,
        'last_updated': last_updated_display
    }
    return render(request, 'joe_rogan/home.html', context=context, )