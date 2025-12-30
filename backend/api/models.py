from django.db import models

class Ingredient(models.Model):
    name = models.CharField(max_length=100)
    quantity = models.CharField(max_length=50, help_text="e.g. 2 kg, 1 packet")
    expiry_date = models.DateField(null=True, blank=True)
    category = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.name

class Recipe(models.Model):
    name = models.CharField(max_length=200)
    instructions = models.TextField(null=True, blank=True)
    cooking_time = models.IntegerField(null=True, blank=True, help_text="Time in minutes")
    spice_level = models.CharField(max_length=50, null=True, blank=True)
    diet_type = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.name

class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='recipe_ingredients')
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    required_qty = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"{self.recipe.name} - {self.ingredient.name}"

class MealHistory(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200)
    date_cooked = models.DateField(auto_now_add=True)
    ingredients_used = models.TextField(blank=True, help_text="List of ingredients used")

    class Meta:
        verbose_name_plural = "Meal Histories"

    def __str__(self):
        return f"{self.name} on {self.date_cooked}"
