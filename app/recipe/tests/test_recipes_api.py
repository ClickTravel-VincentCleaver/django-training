from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Recipe, Ingredient

from recipe.serializers import RecipeSerializer


RECIPES_URL = reverse('recipe:recipe-list')


def recipe_url(recipe_id):
    """Construct URL for a single recipe based on its ID"""
    return reverse('recipe:recipe-detail', args=[recipe_id])


def given_recipe_exists(**params):
    defaults = {
        'name': 'MOCK_RECIPE_NAME',
        'description': 'MOCK_RECIPE_DESCRIPTION'
    }
    defaults.update(params)
    return Recipe.objects.create(**defaults)


def given_ingredient_exists(recipe, **params):
    defaults = {
        'name': 'MOCK_INGREDIENT_NAME',
    }
    defaults.update(params)
    return Ingredient.objects.create(recipe=recipe, **defaults)


class PublicRecipeApiTests(TestCase):
    """Test Recipe public API"""

    def setUp(self):
        self.client = APIClient()

    def test_get_recipes(self):
        """Test GET recipes/"""

        # Given
        given_recipe_exists(name='Eggs Benedict')
        given_recipe_exists(name='Ham Egg and Chips')

        # When
        response = self.client.get(RECIPES_URL)

        # Then the request is successful
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Then the response contains the recipes
        self.assertEqual(response.data[0]['name'], 'Eggs Benedict')
        self.assertEqual(response.data[1]['name'], 'Ham Egg and Chips')

    def test_get_recipes_by_name_filter(self):
        """Test GET recipes/?name=xyz"""

        # Given
        included_recipe1 = given_recipe_exists(name='Strawberry trifle')
        excluded_recipe = given_recipe_exists(name='Orange trifle')
        included_recipe2 = given_recipe_exists(name='Raspberry trifle')

        # When
        name_filter = 'berry'
        response = self.client.get(RECIPES_URL, {'name': name_filter})

        # Then the request is successful
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Then the response contains matching recipes
        filtered_recipes = response.data
        self.assertEqual(len(filtered_recipes), 2)
        self.assertIn(RecipeSerializer(included_recipe1).data, response.data)
        self.assertIn(RecipeSerializer(included_recipe2).data, response.data)

        # Then the response does not contain non-matching recipes
        self.assertNotIn(RecipeSerializer(excluded_recipe).data, response.data)

    def test_get_recipes_by_name_filter_no_match(self):
        """Test GET recipes/?name=xyz with no match found"""

        # Given
        given_recipe_exists(name='Strawberry trifle')
        given_recipe_exists(name='Raspberry trifle')

        # When
        name_filter = 'chocolate'
        response = self.client.get(RECIPES_URL, {'name': name_filter})

        # Then the request is successful
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Then the response contains no recipes
        filtered_recipes = response.data
        self.assertEqual(len(filtered_recipes), 0)

    def test_get_recipe(self):
        """Test GET recipes/{id} for existing recipe"""

        # Given
        recipe = given_recipe_exists(name='Carrot Cake')
        given_ingredient_exists(recipe, name='carrots')

        # When
        response = self.client.get(recipe_url(recipe_id=recipe.id))

        # Then the request is successful
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Then the recipe is returned
        recipe_serializer = RecipeSerializer(recipe)
        self.assertEqual(response.data, recipe_serializer.data)

    def test_get_non_existent_recipe(self):
        """Test GET /recipes/{id} for non-existent recipe"""

        # Given
        recipe_id = 12345

        # When
        response = self.client.get(recipe_url(recipe_id))

        # Then the request fails with "not found" status
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_recipe(self):
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
        response = self.client.post(RECIPES_URL, payload)

        # Then the request is successful
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Then the recipe is created
        recipe = Recipe.objects.get(id=response.data['id'])
        self.assertIsNotNone(recipe)
        self.assertEqual(recipe.name, payload['name'])
        self.assertEqual(recipe.description, payload['description'])

        # Then the ingredients are also created
        self.assertEqual(recipe.ingredients.all().count(), 3)

    def test_create_invalid_recipe(self):
        """Test POST recipes/ with invalid payload"""

        # Given
        payload = {
            'name': '',
            'description': 'blank recipe'
        }

        # When
        response = self.client.post(RECIPES_URL, payload)

        # Then the request fails
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_recipe(self):
        """Test PATCH recipes/{id}"""

        # Given
        recipe = given_recipe_exists(name='Shepherds pie')
        given_ingredient_exists(recipe, name='Lamb mince')
        given_ingredient_exists(recipe, name='Mashed potato')

        # When
        new_description = 'This is a new description'
        new_ingredient_name = 'Onions'
        payload = {
            'name': recipe.name,
            'description': new_description,
            'ingredients': [
                {'name': new_ingredient_name}
            ]
        }
        response = self.client.patch(recipe_url(recipe.id), payload)

        # Then the request is successful
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Then the recipe is updated
        recipe.refresh_from_db()
        self.assertEqual(recipe.description, new_description)

        # Then the ingredients are also updated
        self.assertEqual(len(recipe.ingredients.all()), 1)
        self.assertEqual(recipe.ingredients.first().name, new_ingredient_name)

    def test_delete_recipe(self):
        """Test DELETE /recipes/{id} for existing recipe and ingredients"""

        # Given
        recipe_id = 12345
        recipe = given_recipe_exists(id=recipe_id, name='Ravioli')
        given_ingredient_exists(recipe, name='tomatoes')
        given_ingredient_exists(recipe, name='onions')

        # When
        response = self.client.delete(recipe_url(recipe_id))

        # Then the request is successful
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Then the recipe is deleted
        recipes = Recipe.objects.all()
        self.assertEqual(len(recipes), 0)

        # Then the ingredients are also deleted
        ingredients = Ingredient.objects.all()
        self.assertEqual(len(ingredients), 0)

    def test_delete_non_existent_recipe(self):
        """Test DELETE /recipes/{id} for non-existent recipe"""

        # Given no recipe exists
        recipe_id = 12345

        # When
        response = self.client.delete(recipe_url(recipe_id))

        # Then the request fails with "not found" status
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
