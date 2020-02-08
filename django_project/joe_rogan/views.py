from django.shortcuts import render
from django.conf import settings
from django.core.paginator import Paginator
import os

BASE_DIR = settings.BASE_DIR


def home(request):
    filepath = os.path.join(BASE_DIR, 'joe_rogan', 'joe_rogan.csv')
    with open(filepath, 'r') as f:
        quotes = [line for line in f]

    paginator = Paginator(quotes, 50)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'title': "Joe \"Joe Rogan\" Rogan",
        'page_obj': page_obj
    }
    return render(request, 'joe_rogan/home.html', context=context, )