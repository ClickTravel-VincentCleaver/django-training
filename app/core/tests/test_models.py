from django.test import TestCase
from core import models


from recipe.tests.test_recipes_api import given_recipe_exists


class ModelTests(TestCase):

    # -------------------------------
    # model: RECIPE
    # -------------------------------

    def test_recipe_str(self):
        """Test the recipe string representation"""
        recipe = models.Recipe.objects.create(
            name='Chocolate Cake',
            description='Description goes here'
        )

        self.assertEqual(str(recipe), recipe.name)

    # -------------------------------
    # model: INGREDIENT
    # -------------------------------

    def test_ingredient_str(self):
        """Test the ingredient string representation"""
        recipe = given_recipe_exists()
        ingredient = models.Ingredient.objects.create(
            name='Chocolate',
            recipe=recipe,
        )

        self.assertEqual(str(ingredient), ingredient.name)
