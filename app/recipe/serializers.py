from rest_framework import serializers

from core.models import Recipe, Ingredient


class RecipeSerializer(serializers.ModelSerializer):
    """Serializer for Recipe object"""

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'description')
        read_only_fields = ('id',)


class IngredientSerializer(serializers.ModelSerializer):
    """Serializer for Ingredient object"""

    class Meta:
        model = Ingredient
        fields = ('id', 'name')
        read_only_fields = ('id',)
