from django.db import models
from django.core.exceptions import ValidationError, ObjectDoesNotExist


class Ingredient(models.Model):
    name = models.CharField(max_length=80, unique=True)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    title = models.CharField(max_length=120)
    description = models.TextField()
    ingredients = models.ManyToManyField(Ingredient, through='Measure')

    def __str__(self):
        return self.title

    def gen_initial_form_data(self):
        initial = [{'name': i.ingredient.name, 
                    'measure': i.measure} for i in self.measure_set.all()]
        initial.append({'title': self.title, 'description': self.description})
        return initial

    def update_ingredients(self, new_ingredients):
        current = {i.ingredient.name: i.measure for i in
                   self.measure_set.all()}
        removed = []
        for i in current:
            if i not in new_ingredients:
                removed += current.pop(i)
        current.update(new_ingredients)
        for i in current:
            ingredient = Ingredient.objects.get_or_create(name=i)[0]
            try:
                self.measure_set.get(ingredient=ingredient)
            except
            try:
                self.measure_set.create(ingredient=ingredient,
                                        measure=current[i])
            except ValidationError:
                m = self.measure_set.get(ingredient=ingredient)
                m.measure = current[i]
                m.save()
        for i in removed:
            ingredient = Ingredient.objects.get(name=i)
            self.measure_set.get(ingredient=ingredient).delete()

class Measure(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    measure = models.CharField(max_length=120)

    # def save(self, **kwargs):
    #     ingredient = self.ingredient
    #     recipe = self.recipe
    #     if ingredient in recipe.ingredients.all():
    #         raise ValidationError('Ingredient is already in this recipe')
    #         return
    #     super(Measure, self).save()


    def __str__(self):
        return self.recipe.title + " | "  + self.ingredient.name + " :" + self.measure
