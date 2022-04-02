from django import forms
from users.models import User


class UserLoginForm(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(
        min_length=8, required=True,
        widget=forms.PasswordInput,
        label="Password")