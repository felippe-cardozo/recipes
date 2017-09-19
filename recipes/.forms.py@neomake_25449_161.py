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
    confirm_password = forms.CharField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean(self):
        cleaned_data = super(UserForm, self).clean()
        password = clean_data.get('password')
        confirmation = clean_data.get('password')
        if password != confirmation:
            raise forms.ValidationError


IngredientFormSet = formset_factory(IngredientForm, extra=2)
IngredientUpdateSet = formset_factory(IngredientForm, extra=0)
