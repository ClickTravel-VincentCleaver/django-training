from rest_framework import viewsets

from core.models import Recipe, Ingredient
from recipe import serializers


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = serializers.RecipeSerializer

    def perform_create(self, serializer):
        """Create a new Recipe object"""
        serializer.save()


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = serializers.IngredientSerializer

    def perform_create(self, serializer):
        """Create a new Ingredient object"""
        serializer.save()
