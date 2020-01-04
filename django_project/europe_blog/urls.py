from django.urls import path
from .views import (
    EuropePostListView,
    EuropePostSearchView,
    EuropePostCreateView,
    EuropePostDetailView,
    EuropePostUpdateView,
    EuropePostDeleteView
)

urlpatterns = [
    # Eg: /europe_blog
    path('', EuropePostListView.as_view(), name='europe_blog_home'),
    # Eg: /europe_blog/post/new
    path('post/new/', EuropePostCreateView.as_view(), name='europe_post_create'),
    # Eg: /europe_blog/post/6
    path('post/<int:pk>/', EuropePostDetailView.as_view(), name='europe_post_detail'),
    # Eg: /europe_blog/post/6/update
    path('post/<int:pk>/update/', EuropePostUpdateView.as_view(), name='europe_post_update'),
    # Eg: /europe_blog/post/6/delete
    path('post/<int:pk>/delete/', EuropePostDeleteView.as_view(), name='europe_post_delete'),
    # Eg: /europe_blog/search?q=geneva
    path('search', EuropePostSearchView.as_view(), name='europe_post_search')
]