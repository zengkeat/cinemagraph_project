from django.conf.urls import url
from . import views
from django.urls import path, re_path
app_name = 'accounts'

# inside the django rest framework must use the regular expression url(old one) works better,
# cant use the path('<int:pk>',views.PostDetailAPIView.as_view(), name='post_api_detail'),
# the new url version wont work for detail view or any view that require the pk.
# but if the url doesnt required pk/id or slug, it work fine like the CreateAPIView.
urlpatterns = [
    # CraeteAPIView
    url(r'^register/$', views.AccountRegisterAPIView.as_view(), name='accounts_register'),

    url(r'^login/$', views.AccountLoginAPIView.as_view(), name='accounts_login'),

    # # RetrieveAPIView or Detail view
    # url(r'^(?P<pk>\d+)/$',views.CommentDetailAPIView.as_view(), name= 'comment_api_detail'),
    # # UpdateAPIView
    # url(r'^(?P<pk>\d+)/update/$',views.CommentUpdateAPIView.as_view(), name= 'comment_api_update'),



]
