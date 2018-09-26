from django.conf.urls import url
from . import views
from django.urls import path



app_name = 'user_profile'

urlpatterns = [
    url('profile/', views.UserProfileView.as_view(), name='profile'),
    url('edit/', views.UserProfileEdit, name = 'edit'),
    path('<int:pk>', views.UserProfileDetail, name = 'profile_detail'),
    url('follower/', views.FollowerView.as_view(), name = 'follower'),

]
