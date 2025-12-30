from django.urls import path
from .views import IngredientListCreateView, IngredientDetailView, MealHistoryListCreateView
from .agent_views import AgentChatView, AgentInventoryView, AgentRecentMealsView
from .suggestion_views import DirectSuggestionView

urlpatterns = [
    # Ingredient & History APIs
    path('ingredients/', IngredientListCreateView.as_view(), name='ingredient-list-create'),
    path('ingredients/<int:pk>/', IngredientDetailView.as_view(), name='ingredient-detail'),
    path('history/', MealHistoryListCreateView.as_view(), name='meal-history'),
    
    # Agent APIs
    path('agent/chat/', AgentChatView.as_view(), name='agent-chat'),
    path('agent/inventory/', AgentInventoryView.as_view(), name='agent-inventory'),
    path('agent/recent-meals/', AgentRecentMealsView.as_view(), name='agent-recent-meals'),
    path('agent/suggestions/', DirectSuggestionView.as_view(), name='direct-suggestions'),
]
