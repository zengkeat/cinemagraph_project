from django.shortcuts import render
from .forms import RegisterForm
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy


# https://github.com/django/django/blob/master/django/views/generic/edit.py
# CreateView creating a new object, with a response rendered by a template.
# advantage of CreateView is it will help you create a view for create and saving into database, so you no need to
# code out and save yourself
# default template_name_suffix = '_form'
class RegisterView(CreateView):
    form_class = RegisterForm

    # this line tell the server after success POST, what pages should it go.
    # must use reverse_lazy() instead of reverse() in CreateView or (CBV), othervise cannot runserver
    success_url = reverse_lazy('login')

    template_name = 'accounts/register.html'
