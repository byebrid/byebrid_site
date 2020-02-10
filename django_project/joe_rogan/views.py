from django.shortcuts import render
from django.conf import settings
from django.core.paginator import Paginator
from django.views.generic import ListView
import os
import datetime
import pytz
import json

from .models import JoeRoganPost

BASE_DIR = settings.BASE_DIR


class JoeRoganListView(ListView):
    model = JoeRoganPost
    context_object_name = 'video'
    template_name = 'joe_rogan/home.html'

    paginate_by = 5

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)

        # Adding last_updated attribute to know when json was last modified
        filepath = os.path.join(BASE_DIR, 'joe_rogan', 'joe_rogan.json')
        last_updated_time = os.path.getmtime(filepath)
        tz = pytz.timezone('Australia/Melbourne')
        last_updated_date = datetime.datetime.fromtimestamp(last_updated_time, tz)
        last_updated_display = last_updated_date.strftime('%a %-d %b, %Y')

        context['last_updated'] = last_updated_display
        return context