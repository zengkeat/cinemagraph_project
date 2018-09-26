from django.conf.urls import url
from . import views

#FOR LoginView AND LogoutView
from django.contrib.auth import views as auth_views

app_name = 'accounts'

urlpatterns = [
    url('register/', views.RegisterView.as_view(), name='register'),

    # django built in LoginView help us with login without creating a actual view, because login views
    # is too common, so django have built in already.( with database authentication )
    # just supply the template should be render, and the default template tag is {{form}}.
    url("login/", auth_views.LoginView.as_view(template_name="accounts/login.html"),name='login'),

    # LogoutView doesnt need a template to render because logout can just redirect to home
    url("logout/", auth_views.LogoutView.as_view(),name='logout'),

]
