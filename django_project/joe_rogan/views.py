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
        context = super().get_context_data(**kwargs)
        
        last_modified = JoeRoganPost.posts.first().modified
        tz = pytz.timezone('Australia/Melbourne')
        last_modified = last_modified.astimezone(tz)
        last_modified_str = last_modified.strftime('%a %-d %b, %Y')

        context['last_updated'] = last_modified_str
        return context
