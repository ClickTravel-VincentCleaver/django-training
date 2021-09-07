from rest_framework import serializers

from core.models import Recipe, Ingredient


class IngredientSerializer(serializers.ModelSerializer):
    """Serializer for Ingredient object"""

    class Meta:
        model = Ingredient
        fields = ('name',)
        read_only_fields = ('id',)


class RecipeSerializer(serializers.ModelSerializer):
    """Serializer for Recipe object"""
    ingredients = IngredientSerializer(many=True, read_only=False)

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'description', 'ingredients')
        read_only_fields = ('id',)

    def create(self, validated_data):
        ingredients_data = validated_data.pop('ingredients', [])
        recipe = Recipe.objects.create(**validated_data)
        for ingredient in ingredients_data:
            Ingredient.objects.create(recipe=recipe, **ingredient)
        return recipe

    def update(self, instance, validated_data):
        ingredients_data = validated_data.pop('ingredients', [])
        recipe = super().update(instance, validated_data)

        recipe.ingredients.all.delete()
        for ingredient in ingredients_data:
            Ingredient.objects.create(recipe=recipe, **ingredient)
        return recipe
