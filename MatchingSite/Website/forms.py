from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class RegisterForm(UserCreationForm):
    # declare the fields you will show
    username = forms.CharField(label="Your Username")
    # first password field
    password1 = forms.CharField(label="Your Password", widget=forms.PasswordInput)
    # confirm password field
    password2 = forms.CharField(label="Repeat Your Password", widget=forms.PasswordInput)
    email = forms.EmailField(label = "Email Address")
    first_name = forms.CharField(label = "Name")
    last_name = forms.CharField(label = "Surname")

    def is_valid(self):
        return 1


    # this sets the order of the fields
    def clean_username(self):
        username = self.cleaned_data['username'].lower()
        r = User.objects.filter(username=username)
        if r.count():
            raise  ValidationError("Username already exists")
        return username

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        r = User.objects.filter(email=email)
        if r.count():
            raise  ValidationError("Email already exists")
        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise ValidationError("Password don't match")

        return password2

    def save(self, commit=True):
        user = User.objects.create_user(
            self.cleaned_data['username'],
            self.cleaned_data['email'],
            self.cleaned_data['password1']
        )
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
