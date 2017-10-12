from django import template

register = template.Library()


@register.simple_tag
def user_likes(user, recipe_id):
    if user.user_likes.filter(id=recipe_id):
        return True
    return False


@register.simple_tag
def user_cookbook(user, recipe_id):
    if user.cookbook.filter(id=recipe_id):
        return True
    return False
