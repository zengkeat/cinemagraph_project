"""testing_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.urls import path, include
from .views import HomeView
from user_profile import views

# for displayng images or files when u click the images in the database
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomeView.as_view(), name='home'),
    path('accounts/',include('accounts.urls',namespace = 'accounts')),
    path('user_profile/', include('user_profile.urls' , namespace='user_profile')),
    path('post/', include('post.urls', namespace='post')),
    path('article/', include('article.urls', namespace='article')),
    # url specific for following user
    path('follow/', views.ProfileFollowerToggle.as_view(), name= 'follow'),
    # Home feed from user_profile.views
    path('home/', views.HomeFeedView.as_view(), name = 'home-feed'),
    # post rest api
    path('api/post/',include('post.api.urls', namespace='post-api')),
    # comment rest api
    path('api/comment/',include('comment.api.urls', namespace='comment-api')),
    # accounts rest api
    path('api/accounts/',include('accounts.api.urls', namespace='accounts-api')),

    # to use the auth app we need to add it to our project-level urls.py file.
    # like django.contrib.auth built in LoginView
    #https://wsvincent.com/django-user-authentication-tutorial-login-and-logout/
    path('accounts/', include('django.contrib.auth.urls')),
    # add django-ckeditor URLs to sitewide urls.py file.
    path('ckeditor/', include('ckeditor_uploader.urls')),



]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    # ** for displayng images or files when u click the images in the database**
