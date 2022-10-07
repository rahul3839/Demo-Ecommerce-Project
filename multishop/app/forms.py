from django import forms
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm,UsernameField 
from django.utils.translation import gettext, gettext_lazy as _
from .models import CustomUser
from app import models

#-------------------USER LOGIN-----------------------
class LoginForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(attrs={'autofocus': True}))
    password = forms.CharField(

        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password'}),
        
    )
#-----------------------USER REGISTRATION--------------------------------    
class UserForm(UserCreationForm): 
    class Meta:
        model =CustomUser
        fields = ('username','first_name','last_name','email','mobile')
    labels = {'email':'Email'}

#---------------------USER PROFILE UPDATE--------------------------------------------- 
class UserUpdatForm(UserForm):
    password = None
    class Meta:
        model = CustomUser
        fields = ['username','first_name','last_name','email','mobile']
        labels = {'email':'Email'}
