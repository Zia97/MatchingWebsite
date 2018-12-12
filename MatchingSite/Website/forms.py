from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.forms.widgets import DateInput,SelectDateWidget
from django.forms.widgets import Select, Widget
import datetime


class RegisterForm(UserCreationForm):
    username = forms.CharField(label="Your Username")
    password1 = forms.CharField(label="Your Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Repeat Your Password", widget=forms.PasswordInput)
    image = forms.FileField(widget=forms.FileInput(attrs={'id':'image'}))
    sex = forms.ChoiceField(choices=[("m","Male"),("f","Female")])
    dayRange = range(1,32)
    birthdate = forms.DateField(widget=SelectDateWidget(years=range(1900, 2100)))
    email = forms.EmailField(label = "Email Address")
    first_name = forms.CharField(label = "Name")
    last_name = forms.CharField(label = "Surname")
    HOBBY_CHOICES = (
        ('Running', 'Running'),
        ('Cycling', 'Cycling'),
        ('Gaming','Gaming'),
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

    def is_valid(self):
        return 1


    #def cleaned_data(self)


    #this sets the order of the fields
    # @Overrid
    # def clean_username(self):
    #     username = self.cleaned_data.get('username').lower()
    #     r = User.objects.filter(username=username)
    #     if r.count():
    #         raise  ValidationError("Username already exists")
    #     return username
    #
    # def clean_email(self):
    #     email = self.cleaned_data.get('email').lower()
    #     r = User.objects.filter(email=email)
    #     if r.count():
    #         raise  ValidationError("Email already exists")
    #     return email
    #
    # def clean_password2(self):
    #     password1 = self.cleaned_data.get('password1')
    #     password2 = self.cleaned_data.get('password2')
    #
    #     if password1 and password2 and password1 != password2:
    #         raise ValidationError("Password don't match")
    #
    #     return password2

    #def cleaned_data(self)

    class DateInput(forms.DateInput):
        input_type = 'date'

    def save(self, commit=True):
        user=super(UserCreationForm, self).save(commit=True)
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


    # this redefines the save function to include the fields you added
    # def save(self, commit=True):
    #     user = super(UserCreateForm, self).save(commit=False)
    #     user.email = self.cleaned_data["email"]
    #     user.first_name = self.cleaned_data["first_name"]
    #     user.last_name = self.cleaned_data["last_name"]
    #     if commit:
    #         user.save()
    #         return user
