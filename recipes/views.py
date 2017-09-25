from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .forms import RecipeForm, IngredientFormSet, IngredientUpdateSet,\
                   UserForm, LoginForm
from .models import Ingredient, Measure, Recipe


@login_required
def log_out(request):
    logout(request)
    return redirect('index')


def log_in(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data.get('username'),
                                password=form.cleaned_data.get('password'))
            if user:
                if user.is_active:
                    login(request, user)
                    return redirect('index')
    return render(request, 'recipes/login.html', {'form': form})


def register(request):
    form = UserForm()
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.set_password(user.password)
            user.save()
            return redirect('index')
    return render(request, 'recipes/register.html', {'form': form})


def index(request):
    recipes = Recipe.objects.all()[:10]
    recipe_col = [{'recipe': recipe, 'ingredients': recipe.measure_set.all()}
                  for recipe in recipes]
    return render(request, 'recipes/index.html', {'recipe_col': recipe_col,
                                                  'title': 'Index'})


@login_required
def new(request):
    form = RecipeForm()
    formset = IngredientFormSet()
    if request.method == 'POST':
        form = RecipeForm(request.POST)
        formset = IngredientFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            recipe = form.save(commit=False)
            author = request.user
            recipe.author = author
            recipe.save()
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
    if request.method == 'POST':
        form = RecipeForm(request.POST, instance=recipe)
        formset = IngredientUpdateSet(request.POST)
        # if form.is_valid() and formset.is_valid():
        if form.is_valid():
            recipe = form.save()
            new_ingredients = {}
            for f in formset:
                if f.is_valid():
                    new_ingredients[f.cleaned_data.get('name')] = \
                            f.cleaned_data.get('measure')
            # new_ingredients = {i.cleaned_data.get('name'):
            #                    i.cleaned_data.get('measure') for i in formset
            #                    if i.cleaned_data.get('name')}
            if new_ingredients:
                recipe.update_ingredients(new_ingredients)
            return redirect('detail', recipe_id=recipe.id)
    form = RecipeForm(instance=recipe)
    initial_data = recipe.gen_initial_form_data()
    formset = IngredientUpdateSet(initial=initial_data)
    return render(request, 'recipes/update.html', {'form': form,
                                                   'formset': formset})


def detail(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    ingredients = [i for i in recipe.measure_set.all()]
    return render(request, 'recipes/detail.html', {'recipe': recipe,
                                                   'ingredients': ingredients})


@login_required
def like(request, recipe_id):
    if request.method == 'POST':
        recipe = Recipe.objects.get(pk=recipe_id)
        recipe.likes.add(request.user)
    return redirect('detail', recipe_id=recipe_id)


@login_required
def unlike(request, recipe_id):
    if request.method == 'POST':
        recipe = Recipe.objects.get(pk=recipe_id)
        recipe.likes.remove(request.user)
    return redirect('detail', recipe_id=recipe_id)


@login_required
def add_to_cookbook(request, recipe_id):
    if request.method == 'POST':
        recipe = Recipe.objects.get(pk=recipe_id)
        request.user.cookbook.add(recipe)
    return redirect('detail', recipe_id=recipe_id)


@login_required
def remove_from_cookbook(request, recipe_id):
    if request.method == 'POST':
        recipe = Recipe.objects.get(pk=recipe_id)
        request.user.cookbook.remove(recipe)
    return redirect('detail', recipe_id=recipe_id)


@login_required
def mycookbook(request):
    recipes = request.user.cookbook.all()
    recipe_col = [{'recipe': recipe, 'ingredients': recipe.measure_set.all()}
                  for recipe in recipes]
    return render(request, 'recipes/index.html', {'recipe_col': recipe_col,
                                                  'title': 'MyCookBook'})


def results(request):
    q = request.GET['q']
    ,
