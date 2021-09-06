from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Ingredient

from recipe.serializers import IngredientSerializer


INGREDIENTS_URL = reverse('recipe:ingredient-list')


def ingredient_url(ingredient_id):
    """Construct URL for a single ingredient based on its UUID"""
    return reverse('recipe:ingredient-detail', args=[ingredient_id])


def given_ingredient_exists(**params):
    defaults = {
        'name': 'MOCK_NAME',
    }
    defaults.update(params)
    return Ingredient.objects.create(**defaults)


class PublicIngredientApiTests(TestCase):
    """Test Ingredient public API"""

    def setUp(self):
        self.client = APIClient()

    def test_get_ingredients(self):
        """Test GET ingredients"""

        # Given
        given_ingredient_exists(name='Eggs')
        given_ingredient_exists(name='Tomatoes')

        # When
        response = self.client.get(INGREDIENTS_URL)

        # Then the request is successful
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Then the response contains the ingredients
        expected_ingredients = Ingredient.objects.all()
        serializer = IngredientSerializer(expected_ingredients, many=True)
        self.assertEqual(response.data, serializer.data)

    def test_get_ingredient(self):
        """Test GET ingredients/{id} for existing ingredient"""

        # Given
        ingredient = given_ingredient_exists(name='Butter')

        # When
        response = self.client.get(ingredient_url(ingredient_id=ingredient.id))

        # Then the request is successful
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Then the ingredient is returned
        serializer = IngredientSerializer(ingredient)
        self.assertEqual(response.data, serializer.data)

    def test_get_non_existent_ingredient(self):
        """Test GET /ingredients/{id} for non-existent ingredient"""

        # Given
        ingredient_id = 12345

        # When
        response = self.client.get(ingredient_url(ingredient_id))

        # Then the request fails with "not found" status
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_post_ingredient(self):
        """Test POST ingredients/"""

        # Given
        payload = {
            'name': 'Potatoes',
        }

        # When
        response = self.client.post(INGREDIENTS_URL, payload)

        # Then the request is successful
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Then the ingredient is created
        ingredient = Ingredient.objects.get(id=response.data['id'])
        self.assertIsNotNone(ingredient)
        self.assertEqual(ingredient.name, payload['name'])

    def test_delete_ingredient(self):
        """Test DELETE /ingredient/{id} for existing ingredient"""

        # Given
        ingredient_id = 12345
        given_ingredient_exists(id=ingredient_id, name='Avocados')

        # When
        response = self.client.delete(ingredient_url(ingredient_id))

        # Then the request is successful
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Then the ingredient is deleted
        ingredients = Ingredient.objects.all()
        self.assertEqual(len(ingredients), 0)

    def test_delete_ingredient_not_found(self):
        """Test DELETE /ingredients/{id} for non-existent ingredients"""

        # Given no ingredient exists
        ingredient_id = 12345

        # When
        response = self.client.delete(ingredient_url(ingredient_id))

        # Then the request fails with "not found" status
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
