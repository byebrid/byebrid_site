from django.shortcuts import render
from django.conf import settings
from django.core.paginator import Paginator
from django.views.generic import ListView
from django.db.models import Q # for querysets
import os
import datetime
import pytz
import json
import dateutil.parser

from .models import JoeRoganPost

BASE_DIR = settings.BASE_DIR
PAGINATE_BY = 5

class JoeRoganListView(ListView):
    model = JoeRoganPost
    context_object_name = 'video'
    template_name = 'joe_rogan/home.html'
    ordering = 'modified'

    paginate_by = PAGINATE_BY

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        last_modified = JoeRoganPost.posts.first().modified
        tz = pytz.timezone('Australia/Melbourne')
        last_modified = last_modified.astimezone(tz)
        last_modified_str = last_modified.strftime('%a %-d %b, %Y')

        context['last_updated'] = last_modified_str
        return context


class JoeRoganSearchView(ListView):
    model = JoeRoganPost
    template_name = 'joe_rogan/home.html'

    paginate_by = PAGINATE_BY

    def get_queryset(self):
        query = self.request.GET.get('q')

        result = JoeRoganPost.posts.filter(
            Q(title__icontains=query) | Q(_quotes__icontains=query)
        )
        
        return result.order_by('-created')