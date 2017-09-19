from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from django.utils import timezone


class Ingredient(models.Model):
    name = models.CharField(max_length=80, unique=True)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    author = models.ForeignKey(User)
    likes = models.ManyToManyField(User, related_name='User_likes')
    title = models.CharField(max_length=120)
    description = models.TextField()
    ingredients = models.ManyToManyField(Ingredient, through='Measure')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(null=True)

    def __str__(self):
        return self.title

    def save(self, **kwargs):
        if self.id:
            self.updated_at = timezone.now()
        else:
            self.created_at = timezone.now()
            super(Recipe, self).save()

    def gen_initial_form_data(self):
        initial = [{'name': i.ingredient.name,
                    'measure': i.measure} for i in self.measure_set.all()]
        initial.append({'title': self.title, 'description': self.description})
        return initial

    def update_ingredients(self, new_ingredients):
        current = {i.ingredient.name: i.measure for i in
                   self.measure_set.all()}
        remove = []
        for i in current:
            if i not in new_ingredients:
                remove.append(i)
        if remove:
            [current.pop(i) for i in remove]
        current.update(new_ingredients)
        for i in current:
            ingredient = Ingredient.objects.get_or_create(name=i)[0]
            try:
                assoc = self.measure_set.get(ingredient=ingredient)
                assoc.measure = current[i]
                assoc.save()
            except ObjectDoesNotExist:
                self.measure_set.create(ingredient=ingredient,
                                        measure=current[i])
        for i in remove:
            ingredient = Ingredient.objects.get(name=i)
            self.measure_set.get(ingredient=ingredient).delete()


class Measure(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    measure = models.CharField(max_length=120)

    def __str__(self):
        return f'{self.recipe.title} | {self.ingredient.name} : {self.measure}'
