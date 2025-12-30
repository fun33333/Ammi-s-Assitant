from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Ingredient, MealHistory, Recipe
from .serializers import IngredientSerializer, MealHistorySerializer, RecipeSerializer
from .suggestion_service import get_meal_suggestions

class IngredientListCreateView(generics.ListCreateAPIView):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer

class IngredientDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer

class MealHistoryListCreateView(generics.ListCreateAPIView):
    queryset = MealHistory.objects.all()
    serializer_class = MealHistorySerializer

class RecipeListCreateView(generics.ListCreateAPIView):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer

class RecipeDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer

class MealSuggestionView(APIView):
    """Get meal suggestions based on preferences"""
    
    def post(self, request):
        preferences = {
            'time': request.data.get('time'),
            'spice_level': request.data.get('spice_level'),
            'diet_type': request.data.get('diet_type')
        }
        
        suggestions = get_meal_suggestions(preferences)
        
        # Format response
        result = []
        for item in suggestions:
            result.append({
                'recipe': RecipeSerializer(item['recipe']).data,
                'score': item['score'],
                'match_percentage': item['match_percentage'],
                'missing_ingredients': item['missing_ingredients'],
                'expiry_bonus': item['expiry_bonus']
            })
        
        return Response({
            'suggestions': result,
            'count': len(result)
        })
