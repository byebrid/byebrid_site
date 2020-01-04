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
from .models import EuropePost


class EuropePostListView(ListView):
    model = EuropePost
    template_name = 'europe_blog/home.html'
    ordering = ['-date_posted']


class EuropePostDetailView(DetailView):
    model = EuropePost


class EuropePostSearchView(ListView):
    model = EuropePost
    template_name = 'europe_blog/home.html' # same as normal list view

    def get_queryset(self):
        query = self.request.GET.get('q')
        return EuropePost.objects.filter(
            Q(location__icontains=query) | Q(content__icontains=query)
        )


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
