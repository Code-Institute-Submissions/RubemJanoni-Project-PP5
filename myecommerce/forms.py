from django import forms
from django.contrib.auth.models import User
from shop.models import Address


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
            'placeholder': 'Leave a comment',
            'rows': 6, 'style': 'resize: none;'})
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



class RegisterForm(forms.Form):
    model = User  # Se estiver associado a um modelo, caso contrário, remova esta linha
    fields = ['username', 'email', 'password', 'password2']
    
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'username'})
    )
    email = forms.CharField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'email'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'password'})
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'password'})
    )
   

    def clean_username(self):
        username = self.cleaned_data.get('username')
        user_create = User.objects.filter(username=username)
        if user_create.exists():
            raise forms.ValidationError('This username already exists')
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        email_create = User.objects.filter(email=email)
        if email_create.exists():
            raise forms.ValidationError('This email already exists')
        return email

    def clean_password(self):
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')

        print(f'valor do primeiro {password}')
        print(f'valor do segundo {password2}')

        if password != password2:
            raise forms.ValidationError("As senhas não coincidem.")

        return password 


# Example AddressForm
from django import forms
from shop.models import Address
from django_countries.fields import CountryField

class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['street_address', 'apartment_address',  'zip', 'address_type']

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['street_address', 'apartment_address',  'zip', 'address_type']



