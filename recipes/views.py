from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse, HttpResponse
from .forms import RecipeForm, IngredientFormSet, IngredientUpdateSet,\
                   UserForm, LoginForm
from .models import Ingredient, Measure, Recipe
from .search import get_recipes_from_es, get_suggestions_from_es


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
    q = request.GET.get("search")
    if q:
        recipes = get_recipes_from_es(q)
        return render(request, 'recipes/index.html', {'recipes': recipes})
    return render(request, 'recipes/index.html')


@login_required
def new(request):
    form = RecipeForm()
    formset = IngredientFormSet()
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES)
        formset = IngredientFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            recipe = form.save(commit=False)
            author = request.user
            recipe.author = author
            recipe.save()
            for form in formset:
                if form.is_valid():
                    name = form.cleaned_data.get('name')
                    measure = form.cleaned_data.get('measure')
                    ingredient = Ingredient.objects.get_or_create(name=name)[0]
                    Measure.objects.create(ingredient=ingredient,
                                           recipe=recipe, measure=measure)
            return redirect('detail', recipe_id=recipe.pk)
    return render(request, 'recipes/form.html', {'form': form,
                                                 'formset': formset,
                                                 'title': 'Criar Receita'})


def update(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES, instance=recipe)
        formset = IngredientUpdateSet(request.POST)
        if form.is_valid():
            recipe = form.save()
            new_ingredients = {}
            for f in formset:
                if f.is_valid():
                    new_ingredients[f.cleaned_data.get('name')] = \
                            f.cleaned_data.get('measure')
            if new_ingredients:
                recipe.update_ingredients(new_ingredients)
            recipe.indexing()
            return redirect('detail', recipe_id=recipe.id)
    form = RecipeForm(instance=recipe)
    initial_data = recipe.gen_initial_form_data()
    formset = IngredientUpdateSet(initial=initial_data)
    return render(request, 'recipes/form.html', {'form': form,
                                                 'formset': formset,
                                                 'title': 'Update'})


def detail(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=int(recipe_id))
    ingredients = [i for i in recipe.measure_set.all()]
    return render(request, 'recipes/detail.html', {'recipe': recipe,
                                                   'ingredients': ingredients})


@login_required
def like(request, recipe_id):
    if request.method == 'POST':
        recipe = Recipe.objects.get(pk=recipe_id)
        recipe.likes.add(request.user)
        recipe.indexing()
        return HttpResponse('success')
    return redirect('detail', recipe_id=recipe_id)


@login_required
def unlike(request, recipe_id):
    if request.method == 'POST':
        recipe = Recipe.objects.get(pk=recipe_id)
        recipe.likes.remove(request.user)
        recipe.indexing()
        return HttpResponse('success')
    return redirect('detail', recipe_id=recipe_id)


@login_required
def add_to_cookbook(request, recipe_id):
    if request.method == 'POST':
        recipe = Recipe.objects.get(pk=recipe_id)
        request.user.cookbook.add(recipe)
        return HttpResponse('success')
    return redirect('detail', recipe_id=recipe_id)


@login_required
def remove_from_cookbook(request, recipe_id):
    if request.method == 'POST':
        recipe = Recipe.objects.get(pk=recipe_id)
        request.user.cookbook.remove(recipe)
        return HttpResponse('success')
    return redirect('detail', recipe_id=recipe_id)


@login_required
def mycookbook(request):
    recipes = request.user.cookbook.all()
    recipe_col = [{'recipe': recipe, 'ingredients': recipe.measure_set.all()}
                  for recipe in recipes]
    return render(request, 'recipes/mycookbook.html', {'recipes': recipe_col
                                                       })


def suggestions(request):
    term = request.GET.get('term')
    if term:
        suggestions = get_suggestions_from_es(term)
        return JsonResponse(suggestions, safe=False)
