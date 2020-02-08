from django.shortcuts import render
from django.conf import settings
import os

BASE_DIR = settings.BASE_DIR


def home(request):
    filepath = os.path.join(BASE_DIR, 'joe_rogan', 'joe_rogan.csv')
    with open(filepath, 'r') as f:
        quotes = [line for line in f]

    context = {
        'quotes': quotes,
        'title': "Joe \"Joe Rogan\" Rogan"
    }
    return render(request, 'joe_rogan/home.html', context=context)