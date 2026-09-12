from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from .models import Comment, Post, Profile

User = get_user_model()


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=150, required=False, label="Nome")
    last_name = forms.CharField(max_length=150, required=False, label="Sobrenome")

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "first_name", "last_name", "email", "password1", "password2")


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("first_name", "last_name", "email")


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ("bio", "avatar")
        widgets = {
            "bio": forms.Textarea(attrs={"rows": 3, "maxlength": 160}),
        }


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ("content",)
        labels = {"content": ""}
        widgets = {
            "content": forms.Textarea(
                attrs={
                    "rows": 3,
                    "maxlength": 280,
                    "placeholder": "O que está acontecendo?",
                }
            )
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("content",)
        labels = {"content": ""}
        widgets = {
            "content": forms.TextInput(
                attrs={
                    "maxlength": 280,
                    "placeholder": "Escreva um comentário...",
                }
            )
        }
