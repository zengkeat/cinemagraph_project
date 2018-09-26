from django.conf.urls import url
from . import views
from django.urls import path ,re_path

app_name = 'article'

urlpatterns = [
    url('article_create/', views.ArticleCreate.as_view(), name = 'article_create'),

    #how to use common regular expressions url in diffrent situation:
    # https://www.codingforentrepreneurs.com/blog/common-regular-expressions-for-django-urls/
    re_path(r'^(?P<slug>[\w-]+)/$', views.ArticleDetail.as_view(), name='article_detail'),

    re_path(r'^update/(?P<slug>[\w-]+)/$', views.ArticleUpdate.as_view(), name='article_update'),

    re_path(r'^delete/(?P<slug>[\w-]+)/$', views.ArticleDelete.as_view(), name='article_delete'),

]
