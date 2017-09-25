from django.core.exceptions import PermissionDenied
from recipes.models import Recipe


def is_author(function):
    def wrap(request, *args, **kwargs):
        recipe = Recipe.objects.get(pk=kwargs['recipe_id'])
        if recipe.author == request.user:
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap


def has_recipe_in_cookbook(function):
    def wrap(request, *args, **kwargs):
        recipe = Recipe.objects.get(pk=kwargs['recipe_id'])
        if recipe in request.user.cookbook.all():
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap
