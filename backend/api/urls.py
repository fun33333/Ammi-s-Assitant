from django.urls import path
from .views import (
    IngredientListCreateView, IngredientDetailView, 
    MealHistoryListCreateView,
    RecipeListCreateView, RecipeDetailView,
    MealSuggestionView
)

urlpatterns = [
    path('ingredients/', IngredientListCreateView.as_view(), name='ingredient-list-create'),
    path('ingredients/<int:pk>/', IngredientDetailView.as_view(), name='ingredient-detail'),
    path('history/', MealHistoryListCreateView.as_view(), name='meal-history'),
    path('recipes/', RecipeListCreateView.as_view(), name='recipe-list-create'),
    path('recipes/<int:pk>/', RecipeDetailView.as_view(), name='recipe-detail'),
    path('suggestions/', MealSuggestionView.as_view(), name='meal-suggestions'),
]
