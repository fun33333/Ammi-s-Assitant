from rest_framework import serializers
from .models import Ingredient, MealHistory

class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = '__all__'

class MealHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = MealHistory
        fields = '__all__'
