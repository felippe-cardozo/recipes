from django import forms
from django.forms import formset_factory
from .models import Recipe


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['title', 'description']


class IngredientForm(forms.Form):
    name = forms.CharField(max_length=120)
    measure = forms.CharField(max_length=120)


class UserForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput)


IngredientFormSet = formset_factory(IngredientForm, extra=2)
IngredientUpdateSet = formset_factory(IngredientForm, extra=0)
