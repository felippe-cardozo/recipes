from django.db import models


class Ingredient(models.Model):
    name = models.CharField(max_length=80)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    title = models.CharField(max_length=120)
    description = models.TextField()
    ingredients = models.ManyToManyField

    def __str__(self):
        return self.title
