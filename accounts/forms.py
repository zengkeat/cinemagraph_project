from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.core.exceptions import ValidationError


# This RegisterForm use the combination of UserCreationForm (a ModelForm)and built in User model.
# UserCreationForm provide pre-done form with username, password1 and password2 (with authentication.)
# Django built in User model provide field of username, first_name, last_name, email field.
# so combination of User model field with UserCreationForm save us alot of time for authenticatetion
# two password field and create another model, because User model is built in.
# The model is DJANGO DEFAULT USER, so no need to register at admin
class RegisterForm(UserCreationForm):
    username = forms.CharField(max_length=100, required= True)
    first_name = forms.CharField(max_length=100, required=True)
    last_name = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(max_length=254)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2' ]

    # this part is to check did the email already exists in our database anot.
    # https://www.youtube.com/watch?v=5dtbbImcUCI&list=PLEsfXFp6DpzTOcOVdZF-th7BS_GYGguAS&index=27
    # at time(** 8:10 - 8:50**)
    # def cleaned_email(self):
    #     email = self.cleaned_data.get("email")
    #     email_qs = User.objects.filter(email = email)
    #     if email_qs.exists():
    #         raise forms.ValidationError(' This email already exists!')
    #     return email
