from django.urls import path

from .views import JoeRoganListView, JoeRoganSearchView

urlpatterns = [
    path('', JoeRoganListView.as_view(), name='joe_rogan_home'),
    path('search', JoeRoganSearchView.as_view(), name='joe_rogan_search')
]