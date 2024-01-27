from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class ContactForm(forms.Form):
    email = forms.CharField(
        error_messages={'required': 'This field is mandatory.'},
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Email'}),

    )
    name = forms.EmailField(
        error_messages={'required': 'This field is mandatory.'},
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Name',
            'required': True})
    )
    message = forms.CharField(
        error_messages={'required': 'This field is mandatory.'},
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Leave a comment'})
    )


class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'username'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'password'})
    )


class RegisterForm(UserCreationForm):
    pass
