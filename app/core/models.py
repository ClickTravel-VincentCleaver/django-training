from django.db import models


class Recipe(models.Model):
    """Recipe"""
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    """Ingredient"""
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
