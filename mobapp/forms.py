from django import forms
from django.forms import *


# class UserRegistrar(forms.Form):
#     first_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
#     last_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
#     student_city = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
#     student_street = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
#     email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))
#     password = forms.CharField(required=True, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
#     study_days = forms.IntegerField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
#     price_level = forms.IntegerField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))


#class LoginForm(forms.Form):
    #email = forms.EmailField(required=True, widget=forms.EmailInput())
    #password = forms.CharField(required=True, widget=forms.PasswordInput())

class LoginForm(forms.Form):
    id = IntegerField(required=True, widget=TextInput(attrs={'class': 'form-control'}))
    password = CharField(required=True, widget=PasswordInput())
    #type = CharField(required=True)