from django import forms
from django.forms import *


class signUpForm(forms.Form):
    id = IntegerField(required=True, widget=TextInput())
    name = CharField(required=True, widget=TextInput())
    password = CharField(required=True, widget=PasswordInput())


class adminLoginForm(forms.Form):
    id = CharField(required=True, widget=TextInput(attrs={'class': 'form-control'}))
    password = CharField(required=True, widget=PasswordInput(attrs={'class': 'special'}))

class LoginForm(forms.Form):
    id = IntegerField(required=True, widget=TextInput(attrs={'class': 'form-control'}))
    password = CharField(required=True, widget=PasswordInput(attrs={'class': 'form-control'}))
    #type = CharField(required=True)