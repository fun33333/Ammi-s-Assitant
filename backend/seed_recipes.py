import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ammi_assistant.settings')
django.setup()

from api.models import Recipe, Ingredient, RecipeIngredient

# Create ingredients first
ingredients_data = [
    {"name": "Rice", "category": "Grains"},
    {"name": "Chicken", "category": "Meat"},
    {"name": "Tomatoes", "category": "Vegetable"},
    {"name": "Onions", "category": "Vegetable"},
    {"name": "Potatoes", "category": "Vegetable"},
    {"name": "Lentils (Dal)", "category": "Grains"},
    {"name": "Yogurt", "category": "Dairy"},
    {"name": "Ginger Garlic Paste", "category": "Spices"},
    {"name": "Oil", "category": "Cooking"},
    {"name": "Salt", "category": "Spices"},
    {"name": "Red Chili Powder", "category": "Spices"},
    {"name": "Turmeric", "category": "Spices"},
    {"name": "Cumin Seeds", "category": "Spices"},
    {"name": "Coriander", "category": "Herbs"},
    {"name": "Green Chilies", "category": "Spices"},
    {"name": "Eggs", "category": "Dairy"},
    {"name": "Spinach (Palak)", "category": "Vegetable"},
    {"name": "Okra (Bhindi)", "category": "Vegetable"},
    {"name": "Beef", "category": "Meat"},
]

print("Creating ingredients...")
for ing_data in ingredients_data:
    ing, created = Ingredient.objects.get_or_create(
        name=ing_data["name"],
        defaults={"category": ing_data["category"], "quantity": "500g"}
    )
    if created:
        print(f"  Created: {ing.name}")

# Create recipes
recipes_data = [
    {
        "name": "Chicken Biryani",
        "cooking_time": 60,
        "spice_level": "High",
        "diet_type": "Non-Veg",
        "instructions": "1. Marinate chicken with yogurt and spices\n2. Cook rice separately\n3. Layer chicken and rice\n4. Dum cook for 30 minutes",
        "ingredients": ["Rice", "Chicken", "Yogurt", "Onions", "Ginger Garlic Paste", "Oil", "Salt", "Red Chili Powder", "Turmeric"]
    },
    {
        "name": "Daal Chawal",
        "cooking_time": 30,
        "spice_level": "Low",
        "diet_type": "Veg",
        "instructions": "1. Wash and boil lentils\n2. Prepare tadka with cumin and onions\n3. Mix and serve with rice",
        "ingredients": ["Lentils (Dal)", "Rice", "Onions", "Cumin Seeds", "Oil", "Salt", "Turmeric"]
    },
    {
        "name": "Aloo Anda (Potato Egg Curry)",
        "cooking_time": 25,
        "spice_level": "Medium",
        "diet_type": "Veg",
        "instructions": "1. Boil eggs and potatoes\n2. Make curry base with tomatoes and onions\n3. Add eggs and potatoes",
        "ingredients": ["Potatoes", "Eggs", "Tomatoes", "Onions", "Ginger Garlic Paste", "Oil", "Salt", "Red Chili Powder", "Turmeric"]
    },
    {
        "name": "Bhindi Masala (Okra Fry)",
        "cooking_time": 20,
        "spice_level": "Medium",
        "diet_type": "Veg",
        "instructions": "1. Wash and cut bhindi\n2. Fry with onions and tomatoes\n3. Add spices and cook till tender",
        "ingredients": ["Okra (Bhindi)", "Onions", "Tomatoes", "Oil", "Salt", "Red Chili Powder", "Turmeric"]
    },
    {
        "name": "Palak Chicken (Spinach Chicken)",
        "cooking_time": 35,
        "spice_level": "Medium",
        "diet_type": "Non-Veg",
        "instructions": "1. Cook chicken with spices\n2. Prepare spinach puree\n3. Mix together and simmer",
        "ingredients": ["Chicken", "Spinach (Palak)", "Onions", "Ginger Garlic Paste", "Yogurt", "Oil", "Salt", "Red Chili Powder"]
    },
    {
        "name": "Simple Rice with Curry",
        "cooking_time": 20,
        "spice_level": "Low",
        "diet_type": "Veg",
        "instructions": "1. Boil rice\n2. Make simple tomato curry\n3. Serve together",
        "ingredients": ["Rice", "Tomatoes", "Onions", "Oil", "Salt", "Turmeric"]
    },
    {
        "name": "Nihari",
        "cooking_time": 120,
        "spice_level": "High",
        "diet_type": "Non-Veg",
        "instructions": "1. Slow cook beef with special spices\n2. Add fried onions\n3. Garnish with ginger and coriander",
        "ingredients": ["Beef", "Onions", "Ginger Garlic Paste", "Oil", "Salt", "Red Chili Powder", "Coriander"]
    },
]

print("\nCreating recipes...")
for recipe_data in recipes_data:
    recipe, created = Recipe.objects.get_or_create(
        name=recipe_data["name"],
        defaults={
            "cooking_time": recipe_data["cooking_time"],
            "spice_level": recipe_data["spice_level"],
            "diet_type": recipe_data["diet_type"],
            "instructions": recipe_data["instructions"]
        }
    )
    if created:
        print(f"  Created: {recipe.name}")
        
        # Add recipe ingredients
        for ing_name in recipe_data["ingredients"]:
            try:
                ingredient = Ingredient.objects.get(name=ing_name)
                RecipeIngredient.objects.create(
                    recipe=recipe,
                    ingredient=ingredient,
                    required_qty=1.0
                )
            except Ingredient.DoesNotExist:
                print(f"    Warning: Ingredient '{ing_name}' not found")

print("\n✅ Seeding completed!")
print(f"Total Ingredients: {Ingredient.objects.count()}")
print(f"Total Recipes: {Recipe.objects.count()}")
