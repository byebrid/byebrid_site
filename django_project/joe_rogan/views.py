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
