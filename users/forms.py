from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from .models import User


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={"class": "form-control", "placeholder": "Email"})
    )
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Имя пользователя"}
        )
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Пароль"}
        )
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Подтверждение пароля"}
        )
    )

    class Meta:
        model = User
        fields = ["email", "username", "password1", "password2"]


class UserUpdateForm(UserChangeForm):
    password = None  # Убираем поле пароля

    email = forms.EmailField(widget=forms.EmailInput(attrs={"class": "form-control"}))
    username = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))
    phone = forms.CharField(
        required=False, widget=forms.TextInput(attrs={"class": "form-control"})
    )
    country = forms.CharField(
        required=False, widget=forms.TextInput(attrs={"class": "form-control"})
    )

    class Meta:
        model = User
        fields = ["email", "username", "phone", "avatar", "country"]
