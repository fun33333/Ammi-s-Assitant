from django.urls import path
from .views import IngredientListCreateView, IngredientDetailView, MealHistoryListCreateView

urlpatterns = [
    path('ingredients/', IngredientListCreateView.as_view(), name='ingredient-list-create'),
    path('ingredients/<int:pk>/', IngredientDetailView.as_view(), name='ingredient-detail'),
    path('history/', MealHistoryListCreateView.as_view(), name='meal-history'),
]
