from rest_framework import generics
from .models import Ingredient, MealHistory
from .serializers import IngredientSerializer, MealHistorySerializer

class IngredientListCreateView(generics.ListCreateAPIView):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer

class IngredientDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer

class MealHistoryListCreateView(generics.ListCreateAPIView):
    queryset = MealHistory.objects.all()
    serializer_class = MealHistorySerializer
