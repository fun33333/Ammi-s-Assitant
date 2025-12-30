from django.contrib import admin
from .models import Ingredient, MealHistory

@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'quantity', 'expiry_date', 'category')
    search_fields = ('name', 'category')
    list_filter = ('expiry_date',)

@admin.register(MealHistory)
class MealHistoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'date_cooked')
    list_filter = ('date_cooked',)
