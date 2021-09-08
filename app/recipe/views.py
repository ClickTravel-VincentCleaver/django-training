from rest_framework import viewsets

from core.models import Recipe
from recipe import serializers


class RecipeViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.RecipeSerializer

    def get_queryset(self):
        """Get recipe objects including filter"""
        name = self.request.query_params.get('name')
        queryset = Recipe.objects.all()
        if name:
            queryset = Recipe.objects.filter(name__icontains=name)
        return queryset

    def perform_create(self, serializer):
        """Create a new Recipe object"""
        serializer.save()
