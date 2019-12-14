"""django_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.urls import path, include, reverse_lazy
from django.conf import settings
from django.conf.urls.static import static
from users import views as user_views
from index import views as index_views
from django.views.generic import RedirectView
from django.views.decorators.cache import never_cache

from ckeditor_uploader import views as ckeditor_views

urlpatterns = [
    path('', RedirectView.as_view(url=reverse_lazy('index_home'))),

    path('home/', index_views.home, name='index_home'),
    path('blog/', include('blog.urls')),
    path('europe_blog/', include('europe_blog.urls')),
    path('admin/', admin.site.urls),
    path('register/', user_views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('profile/', user_views.profile, name='profile'),

    # Password reset paths
    path('password-reset/', 
        auth_views.PasswordResetView.as_view(
            template_name='users/password_reset.html'), 
        name='password_reset'),
    path('password-reset/done', 
        auth_views.PasswordResetDoneView.as_view(
            template_name='users/password_reset_done.html'), 
        name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', 
        auth_views.PasswordResetConfirmView.as_view(
            template_name='users/password_reset_confirm.html'), 
        name='password_reset_confirm'),
    path('password-reset-complete/', 
        auth_views.PasswordResetCompleteView.as_view(
            template_name='users/password_reset_complete.html'), 
        name='password_reset_complete'),

    # I believe this is required for the widget even if we don't directly access the url 
    path('ckeditor/', include('ckeditor_uploader.urls'))
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)