from django import forms
from django.forms import formset_factory
from django.contrib.auth.models import User
from .models import Recipe


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['title', 'description']


class IngredientForm(forms.Form):
    name = forms.CharField(max_length=120)
    measure = forms.CharField(max_length=120)


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean(self):
        cd = super(UserForm, self).clean()
        password = cd.get('password')
        confirmation = cd.get('password')
        email = cd.get('email')
        if password != confirmation:
            raise forms.ValidationError(
                    "password and confirmation does not match")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("email already registered")


class LoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)


IngredientFormSet = formset_factory(IngredientForm, extra=2)
IngredientUpdateSet = formset_factory(IngredientForm, extra=0)
