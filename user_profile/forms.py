from django.contrib.auth.models import User
from django import forms
from user_profile.models import UserExtraModel
from django.forms import ModelForm
from django.contrib.auth.forms import UserChangeForm

#the advantage of using UserChangeForm is it provide the field like password cannot be edit
# and also provide a message if you want to change password.
class EditForm(UserChangeForm):

    class Meta():
        model = User
        fields = ('first_name', 'last_name', 'email', "password")

#make another forms for extra profile imformation
class UserExtraForm(forms.ModelForm):

    class Meta():
        model = UserExtraModel
        fields = ('image','description','city','website','contact')
