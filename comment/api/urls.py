from django.conf.urls import url
from . import views
from django.urls import path, re_path
app_name = 'comment'

# inside the django rest framework must use the regular expression url(old one) works better,
# cant use the path('<int:pk>',views.PostDetailAPIView.as_view(), name='post_api_detail'),
# the new url version wont work for detail view or any view that require the pk.
# but if the url doesnt required pk/id or slug, it work fine like the CreateAPIView.
urlpatterns = [
    # ListAPIView
    url(r'^$', views.CommentListAPIView.as_view(), name='comment_api_list'),
    # RetrieveAPIView or Detail view
    url(r'^(?P<pk>\d+)/$',views.CommentDetailAPIView.as_view(), name= 'comment_api_detail'),
    # UpdateAPIView
    url(r'^(?P<pk>\d+)/update/$',views.CommentUpdateAPIView.as_view(), name= 'comment_api_update'),
    


]
