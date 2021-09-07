from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Recipe

from recipe.serializers import RecipeSerializer


RECIPES_URL = reverse('recipe:recipe-list')


def recipe_url(recipe_id):
    """Construct URL for a single recipe based on its UUID"""
    return reverse('recipe:recipe-detail', args=[recipe_id])


def given_recipe_exists(**params):
    defaults = {
        'name': 'MOCK_NAME',
        'description': 'MOCK_DESCRIPTION'
    }
    defaults.update(params)
    return Recipe.objects.create(**defaults)


class PublicRecipeApiTests(TestCase):
    """Test Recipe public API"""

    def setUp(self):
        self.client = APIClient()

    def test_get_recipes(self):
        """Test GET recipes"""

        # Given
        given_recipe_exists(name='Eggs Benedict')
        given_recipe_exists(name='Ham Egg and Chips')

        # When
        response = self.client.get(RECIPES_URL)

        # Then the request is successful
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Then the response contains the recipes
        expected_recipes = Recipe.objects.all()
        serializer = RecipeSerializer(expected_recipes, many=True)
        self.assertEqual(response.data, serializer.data)

    def test_get_recipe(self):
        """Test GET recipes/{id} for existing recipe"""

        # Given
        recipe = given_recipe_exists(name='Carrot Cake')

        # When
        response = self.client.get(recipe_url(recipe_id=recipe.id))

        # Then the request is successful
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Then the recipe is returned
        serializer = RecipeSerializer(recipe)
        self.assertEqual(response.data, serializer.data)

    def test_get_non_existent_recipe(self):
        """Test GET /recipes/{id} for non-existent recipe"""

        # Given
        recipe_id = 12345

        # When
        response = self.client.get(recipe_url(recipe_id))

        # Then the request fails with "not found" status
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_post_recipe(self):
        """Test POST recipes/"""

        # Given
        payload = {
            'name': 'Gnocchi',
            'description': 'Basically potatoes but better',
            'ingredients': [
                {'name': 'potatoes'},
                {'name': 'flour'},
                {'name': 'eggs'},
            ]
        }

        # When
        response = self.client.post(
            RECIPES_URL,
            payload,
        )

        # Then the request is successful
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Then the recipe is created
        recipe = Recipe.objects.get(id=response.data['id'])
        self.assertIsNotNone(recipe)
        self.assertEqual(recipe.name, payload['name'])
        self.assertEqual(recipe.description, payload['description'])
        self.assertEqual(recipe.ingredients.all().count(), 3)

    def test_delete_recipe(self):
        """Test DELETE /recipes/{id} for existing recipe"""

        # Given
        recipe_id = 12345
        given_recipe_exists(id=recipe_id, name='Ravioli')

        # When
        response = self.client.delete(recipe_url(recipe_id))

        # Then the request is successful
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Then the recipe is deleted
        recipes = Recipe.objects.all()
        self.assertEqual(len(recipes), 0)

    def test_delete_recipe_not_found(self):
        """Test DELETE /recipes/{id} for non-existent recipe"""

        # Given no recipe exists
        recipe_id = 12345

        # When
        response = self.client.delete(recipe_url(recipe_id))

        # Then the request fails with "not found" status
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
