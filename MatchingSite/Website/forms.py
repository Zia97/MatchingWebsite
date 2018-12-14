from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.forms.widgets import DateInput, SelectDateWidget
from django.forms.widgets import Select, Widget
import datetime


class RegisterForm(UserCreationForm):

    # Implementing and overiding the UserCreationForm to add our own fields
    #Bootstrap added as attributes
    username = forms.CharField(label="Your Username", widget=forms.TextInput(
        attrs={
            'class': "form-control",
            'placeholder': 'Username'
        }
    ))
    password1 = forms.CharField(label="Your Password", widget=forms.PasswordInput(
        attrs={
            'class': "form-control",
            'placeholder': 'Password'
        }
    ))
    password2 = forms.CharField(label="Repeat Your Password", widget=forms.PasswordInput(
        attrs={
            'class': "form-control",
            'placeholder': 'Repeat Password'
        }
    ))
    image = forms.FileField(widget=forms.FileInput(
        attrs={
            'class': "form-control",
            'id': 'image',
        }
    ))
    sex = forms.ChoiceField(choices=[("Male", "Male"), ("Female", "Female")], widget=forms.Select(
        attrs={
            'class': "form-control"
        }
    ))
    birthdate = forms.DateField(widget=SelectDateWidget(
        attrs={
            'class': "form-control"
        },
        years=range(1900, 2018)
    ))
    email = forms.EmailField(label="Email Address", widget=forms.TextInput(
        attrs={
            'class': "form-control",
            'placeholder': 'Email'
        }
    ))
    first_name = forms.CharField(label="Name", widget=forms.TextInput(
        attrs={
            'class': "form-control",
            'placeholder': 'First Name'
        }
    ))
    last_name = forms.CharField(label="Surname", widget=forms.TextInput(
        attrs={
            'class': "form-control",
            'placeholder': 'Last Name'
        }
    ))
    HOBBY_CHOICES = (
        ('Running', 'Running'),
        ('Cycling', 'Cycling'),
        ('Gaming', 'Gaming'),
        ('Music', 'Music'),
        ('Hiking', 'Hiking'),
        ('Painting', 'Painting'),
        ('Dancing', 'Dancing'),
        ('Cooking', 'Cooking'),
        ('Photography', 'Photography'),
        ('Gardening', 'Gardening'),

    )
    hobbies = forms.MultipleChoiceField(
        required=True,
        widget=forms.CheckboxSelectMultiple,
        choices=HOBBY_CHOICES,
    )

    # Saving the user provided all the fields are verified
    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=True)
        user.set_password(self.clean_password2())
        user.username = self.cleaned_data["username"]
        user.email = self.cleaned_data["email"]
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.sex = self.cleaned_data["sex"]
        user.birthdate = self.cleaned_data["birthdate"]
        user.hobbies = self.cleaned_data["hobbies"]
        user.image = self.cleaned_data["image"]

        if commit:
            user.save()
        return user

    # Defined our own email validation and overriden the standard verification
    def clean_email(self):
        email = self.cleaned_data["email"]
        username = self.cleaned_data["username"]
        if email and User.objects.filter(email=email).exclude(username=username).exists():
            raise forms.ValidationError('Email address must be unique')
        return email
