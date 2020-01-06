from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView, 
    DetailView, 
    CreateView, 
    UpdateView,
    DeleteView
)
from django.db.models import Q # for querysets
import datetime
import dateutil.parser
import calendar
from .models import EuropePost


class EuropePostListView(ListView):
    model = EuropePost
    template_name = 'europe_blog/home.html'
    ordering = ['-arrival_date']


class EuropePostDetailView(DetailView):
    model = EuropePost


class EuropePostSearchView(ListView):
    """A view to process the user's search query.
    
    Will attempt to parse dates and find relevant posts. Allows for somewhat
    fuzzy parsing (i.e. assumes year to be 2019 since that was the year of the
    trip) and allows user to simply put in a month (or acceptable shorthand such
    as 'jun' for June) and get all relevant posts.

    Note: If user looks for the word 'may', this will obviously get interpreted as
    the month so tough luck if they want the actual word.
    """
    model = EuropePost
    template_name = 'europe_blog/home.html' # same as normal list view

    def get_queryset(self):
        query = self.request.GET.get('q')

        # Test if user passed in date. If so, test against dates of trip
        try:
            query_as_date = dateutil.parser.parse(query, fuzzy=True)
            query_as_date = query_as_date.replace(year=2019) # trip was in 2019

            # __init__ ensures months are converted to lower-case, which is nice
            parserinfo = dateutil.parser.parserinfo()

            # If user only passes month in, then get all posts for that month
            if query.lower() in parserinfo._months:
                query_month = query_as_date.month # Get the month as int, not str
                start_of_month = datetime.date(2019, query_month, 1)
                # monthrange returns tuple of (first day, last day) in month
                n_days_in_month = calendar.monthrange(2019, query_month)[1]
                end_of_month = datetime.date(2019, query_month, n_days_in_month)

                # Get all posts from sometime in this month
                result = EuropePost.objects.filter(
                    Q(arrival_date__gte=start_of_month, arrival_date__lte=end_of_month) |
                    Q(departure_date__gte=start_of_month, departure_date__lte=end_of_month)
                )
            else:
                result = EuropePost.objects.filter(arrival_date__lte=query_as_date, departure_date__gte=query_as_date)
        except Exception as e:
            print(e)
            # If query not recognised as date, compare with contents of blog posts
            result = EuropePost.objects.filter(
                Q(location__icontains=query) | Q(content__icontains=query)
            )
        
        result = result.order_by('-arrival_date')
        return result


class EuropePostCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = EuropePost
    fields = ['location', 'arrival_date', 'departure_date', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        return self.request.user.is_staff


class EuropePostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = EuropePost
    fields = ['location', 'arrival_date', 'departure_date', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        return post.author == self.request.user


class EuropePostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = EuropePost
    success_url = reverse_lazy('europe_blog_home')

    def test_func(self):
        post = self.get_object()
        return post.author == self.request.user
