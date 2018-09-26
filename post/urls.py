from django.conf.urls import url
from . import views
from django.urls import path
app_name = 'post'

urlpatterns = [
    url('user_post/', views.PostView.as_view(), name= 'user_post'),
    url('post_list/', views.PostList.as_view(), name='post_list'),

    # DetailView url is represent in the post ID, meaning type in the id of the post
    # and show the detail of the specific post, that what DetailView do, for viewing detail of a model.
    # example if you type /post/4 it will take you to the ID 4 post
    # and you can customize the detail you want to show in the detail.html.
    path('<int:pk>', views.PostDetail, name= 'post_detail'),
    path('update/<int:pk>/', views.PostUpdate, name= 'post_update'),

    #django like button RedirectView
    path('<int:pk>/like/', views.PostLikeToggle.as_view(), name= 'like_toggle'),


    ]
