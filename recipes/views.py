from django.shortcuts import render, redirect, get_object_or_404
from .forms import RecipeForm, IngredientFormSet
from .models import Ingredient, Measure, Recipe


def index(request):
    recipes = Recipe.objects.all()[:10]
    measures = [(recipe, recipe.measure_set.all()) for recipe in recipes]
    return render(request, 'recipes/index.html', {'measures': measures})


def new(request):
    form = RecipeForm()
    formset = IngredientFormSet()
    if request.method == 'POST':
        form = RecipeForm(request.POST)
        formset = IngredientFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            recipe = form.save()
            for form in formset:
                name = form.cleaned_data.get('name')
                measure = form.cleaned_data.get('measure')
                ingredient = Ingredient.objects.get_or_create(name=name)[0]
                Measure.objects.create(ingredient=ingredient,
                                       recipe=recipe, measure=measure)
            return redirect('index')
    return render(request, 'recipes/new.html', {'form': form,
                                                'formset': formset})


def update(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    current_ingredients = {i.ingredient.name: i.measure for i in recipe.measure_set.all()}
    form = RecipeForm(instance=recipe)
    initial_data = recipe.gen_initial_form_data()
    formset = IngredientFormSet(initial=initial_data)
    if request.method == 'POST':
        form = RecipeForm(request.POST, instance=recipe)
        formset= IngredientFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            recipe = form.save()
            new_ingredients = {i.cleaned_data.get('name'): 
                               i.cleaned_data.get('measure') for i in formset 
                               if i.cleaned_data.get('name')}
            if new_ingredients == current_ingredients:
                return redirect('detail', recipe_id=recipe.id)
            current_ingredients.update(new_ingredients) 
            for i in recipe.measure_set.all():
                i.delete()
            for i in current_ingredients:
                ingredient = Ingredient.objects.get_or_create(name=i)[0]
                Measure.objects.create(ingredient=ingredient,
                                       measure=current_ingredients.get(i),
                                       recipe=recipe)
            return redirect('detail', recipe_id=recipe.id)
    return render(request, 'recipes/update.html', {'form': form, 'formset': formset})



            
def detail(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    ingredients = [i for i in recipe.measure_set.all()]
    return render(request, 'recipes/detail.html', {'recipe': recipe,
                                                   'ingredients': ingredients})
