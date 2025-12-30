from rest_framework import serializers
from .models import Ingredient, MealHistory, Recipe, RecipeIngredient

class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = '__all__'

class MealHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = MealHistory
        fields = '__all__'

class RecipeIngredientSerializer(serializers.ModelSerializer):
    ingredient_name = serializers.CharField(source='ingredient.name', read_only=True)
    
    class Meta:
        model = RecipeIngredient
        fields = ['id', 'ingredient', 'ingredient_name', 'required_qty']

class RecipeSerializer(serializers.ModelSerializer):
    recipe_ingredients = RecipeIngredientSerializer(many=True, read_only=True)
    
    class Meta:
        model = Recipe
        fields = ['id', 'name', 'instructions', 'cooking_time', 'spice_level', 'diet_type', 'recipe_ingredients']
