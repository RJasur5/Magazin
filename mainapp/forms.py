from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.contenttypes import models
from django.db.models import fields
from django.forms.models import ModelForm

from .models import Customer, Order


class OrderForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['order_date'].label = 'Дата получения заказа'

    order_date = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}))

    class Meta:
        model = Order
        fields = (
            'first_name', 'last_name', 'phone', 'address', 'buying_type', 'order_date', 'comment'
        )


class LoginForm(forms.ModelForm):

    password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Username'


    def clean(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        if not User.objects.filter(username=username).exists():
            raise forms.ValidationError(f'User with logon {username} not found')
        user = User.objects.filter(username=username).first()
        if user:
            if not user.check_password(password):
                raise forms.ValidationError("Invalid Parol")
        return self.cleaned_data


    class Meta:
        model = User
        fields = ['username', 'password']


# class RegistrationForm(UserCreationForm):

#     confirm_password = forms.CharField(widget=forms.PasswordInput)
#     password = forms.CharField(widget=forms.PasswordInput)
#     phone = forms.CharField(required=False)
#     addres = forms.CharField(required=False)
#     email = forms.EmailField(required=True)

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['username'].label = 'Username'

    # def clean_email(self):
    #     email = self.cleaned_data('email')
    #     domain = email.split('.')[-1]
    #     if domain in ['com', 'net']:
    #         raise forms.ValidationError(f'Registratsiya dlya domena {domain} ne vozmojna')
    #     if User.objects.filter(email=email).exists():
    #         raise forms.ValidationError(f'Danniy pochtoviy addres uje zaregestrovan')
    #     return email

    # def clean_username(self):
    #     username = self.cleaned_data('username')
    #     if User.objects.filter(username=username).exists():
    #         raise forms.ValidationError(f'Imya {username} zaneto')
    #     return username
    
    # def clean(self):
    #     password = self.cleaned_data['password']
    #     confirm_password = self.cleaned_data['confirm_password']
    #     if password != confirm_password:
    #         raise forms.ValidationError('Paroli ne sovpadayut')
    #     return self.cleaned_data
    
class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class CustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = "__all__"
