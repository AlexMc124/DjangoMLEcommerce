from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from store.models import Product
from .models import Profile


# USed to make users in the DB
class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']


# Used to update entries in the db
class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']


class ProfileUpdateForm(forms.ModelForm):
    interests = forms.ChoiceField(choices=Profile.INTEREST_CHOICES)

    class Meta:
        model = Profile
        fields = ['profile_image', 'interests']


class ProductCreateForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['asin', 'title', 'price', 'imageUrl', 'brand', 'description', 'details', 'category', 'main_cat']
