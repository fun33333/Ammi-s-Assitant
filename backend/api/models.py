from django.db import models

class Ingredient(models.Model):
    name = models.CharField(max_length=100)
    quantity = models.CharField(max_length=50, help_text="e.g. 2 kg, 1 packet")
    expiry_date = models.DateField(null=True, blank=True)
    category = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.name

class MealHistory(models.Model):
    name = models.CharField(max_length=200)
    date_cooked = models.DateField(auto_now_add=True)
    ingredients_used = models.TextField(blank=True, help_text="List of ingredients used")

    class Meta:
        verbose_name_plural = "Meal Histories"

    def __str__(self):
        return f"{self.name} on {self.date_cooked}"
