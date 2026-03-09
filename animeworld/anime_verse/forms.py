from django import forms
from django.contrib.auth.models import User
from .models import UserProfile, AnimeWorld

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username"]

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        exclude = ["user", "created_at", "is_delete"]
        widgets = {
            "country": forms.Select(attrs={"class": "custom-select"})
        }

class AnimeWorldForm(forms.ModelForm):
    class Meta:
        model = AnimeWorld
        exclude = ['user', 'comics', 'created_at', 'is_trending', 'is_active', 'is_delete']