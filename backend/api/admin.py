from django.contrib import admin
from .models import Ingredient, MealHistory, Recipe, RecipeIngredient

@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'quantity', 'expiry_date', 'category')
    search_fields = ('name', 'category')
    list_filter = ('expiry_date',)

@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'cooking_time', 'spice_level', 'diet_type')
    search_fields = ('name',)
    list_filter = ('spice_level', 'diet_type')

@admin.register(RecipeIngredient)
class RecipeIngredientAdmin(admin.ModelAdmin):
    list_display = ('recipe', 'ingredient', 'required_qty')
    search_fields = ('recipe__name', 'ingredient__name')

@admin.register(MealHistory)
class MealHistoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'date_cooked', 'recipe')
    list_filter = ('date_cooked',)
