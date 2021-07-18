from django.contrib.auth import authenticate
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField, PasswordResetForm
from django.contrib.auth.models import User
from django import forms
from .models import Feedback
from django.forms import ModelForm, fields, widgets
from .models import Contact


class CustomUserCreationForm(forms.Form):
    username = forms.CharField(
        label='Enter Username', min_length=4, max_length=150)
    email = forms.EmailField(label='Enter email')
    password1 = forms.CharField(
        label='Enter password', widget=forms.PasswordInput)
    password2 = forms.CharField(
        label='Confirm password', widget=forms.PasswordInput)

    def clean_username(self):
        username = self.cleaned_data['username'].lower()
        r = User.objects.filter(username=username)
        if r.count():
            raise forms.ValidationError("Username already exists")
        return username

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        r = User.objects.filter(email=email)
        if r.count():
            raise forms.ValidationError("Email already exists")
        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Password don't match")

        return password2

    def save(self, commit=True):
        user = User.objects.create_user(
            self.cleaned_data['username'],
            self.cleaned_data['email'],
            self.cleaned_data['password1']
        )
        return user


class FeedbackForm(forms.ModelForm):

    class Meta:
        model = Feedback
        fields = '__all__'


class ContactForm(forms.Form):

    name = forms.CharField(max_length=50)
    emails = forms.EmailField(max_length=150)
    message = forms.CharField(widget=forms.Textarea, max_length=2000)


class CustomerRegistrationForm(UserCreationForm):
    email = forms.EmailField(
        required=True, label='Email', widget=forms.EmailInput(attrs={'class': 'form-control'}))

    password1 = forms.CharField(
        label='Enter password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(
        label='Confirm password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = {'username', 'email', 'password1', 'password2'}
        # labels = {'email', 'Email'}
        widgets = {'username': forms.TextInput(
            attrs={'class': 'form-control'})}
