from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Watches, Category, ShippingAddress, Customer

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class FurnitureModelForm(forms.ModelForm):
    class Meta:
        model = Watches
        fields = ['title', 'slug', 'description', 'is_published', 'category', 'price', 'photo']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'slug': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'is_published': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'photo': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name','email']
        widgets = {
            'name':forms.TextInput(attrs={
                'class':"form-control",
                'placeholder':"Your name"
            }),
            'email':forms.EmailInput(attrs={
                'class':"form-control",
                'placeholder':"Your email"
            }),
        }

class ShippingAddressForm(forms.ModelForm):
    class Meta:
        model = ShippingAddress
        fields = ['address','city','state','zipcode']
        widgets = {
            'address': forms.TextInput(attrs={
                'class': "form-control",
                'placeholder': "Your address"
            }),
            'city': forms.TextInput(attrs={
                'class': "form-control",
                'placeholder': "Your city"
            }),
            'state': forms.TextInput(attrs={
                'class': "form-control",
                'placeholder': "Your state"
            }),
            'zipcode': forms.TextInput(attrs={
                'class': "form-control",
                'placeholder': "Your zipcode"
            }),
        }