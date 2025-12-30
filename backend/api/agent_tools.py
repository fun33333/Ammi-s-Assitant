from datetime import datetime, timedelta
from django.db.models import Count, Q
from .models import Ingredient, MealHistory
import json
from google import genai
from google.genai import types
import os

# Initialize Gemini client for recipe generation
client = genai.Client(api_key=os.getenv('GEMINI_API_KEY', 'AIzaSyDIxFXJWj4VHXLmxCAZP33yd-u9PjwQOCI'))


def get_current_inventory():
    """Get all ingredients with their details"""
    ingredients = Ingredient.objects.all()
    
    inventory_list = []
    for ing in ingredients:
        item = {
            "name": ing.name,
            "quantity": ing.quantity,
            "category": ing.category
        }
        
        if ing.expiry_date:
            days_to_expiry = (ing.expiry_date - datetime.now().date()).days
            item["expiry_date"] = ing.expiry_date.strftime("%Y-%m-%d")
            item["days_to_expiry"] = days_to_expiry
            
            if days_to_expiry <= 2:
                item["urgency"] = "high"
            elif days_to_expiry <= 5:
                item["urgency"] = "medium"
            else:
                item["urgency"] = "low"
        
        inventory_list.append(item)
    
    return {
        "total_items": len(inventory_list),
        "ingredients": inventory_list
    }


def get_recent_meals(days: int = 3):
    """Get meals cooked in the last N days
    
    Args:
        days: Number of days to look back (default 3)
    """
    cutoff_date = datetime.now().date() - timedelta(days=days)
    recent_meals = MealHistory.objects.filter(
        date_cooked__gte=cutoff_date
    ).order_by('-date_cooked')
    
    meals_list = []
    for meal in recent_meals:
        meals_list.append({
            "name": meal.name,
            "date_cooked": meal.date_cooked.strftime("%Y-%m-%d"),
            "ingredients_used": meal.ingredients_used
        })
    
    return {
        "days_checked": days,
        "total_meals": len(meals_list),
        "meals": meals_list
    }


def suggest_recipes(max_results: int = 3):
    """
    Suggest recipes based on available ingredients
    
    Args:
        max_results: Maximum number of suggestions (default 3)
    """
    inventory = get_current_inventory()
    available_ingredients = [ing["name"].lower() for ing in inventory["ingredients"]]
    
    # Enhanced Pakistani recipe database
    recipe_database = [
        {
            "name": "Daal Chawal",
            "ingredients": ["lentils", "rice", "onions", "oil", "salt"],
            "cooking_time": 30,
            "difficulty": "Easy",
            "category": "Veg"
        },
        {
            "name": "Chicken Biryani",
            "ingredients": ["chicken", "rice", "yogurt", "onions", "biryani masala"],
            "cooking_time": 60,
            "difficulty": "Medium",
            "category": "Non-Veg"
        },
        {
            "name": "Aloo Gobi",
            "ingredients": ["potatoes", "cauliflower", "tomatoes", "onions", "cumin"],
            "cooking_time": 25,
            "difficulty": "Easy",
            "category": "Veg"
        },
        {
            "name": "Palak Chicken",
            "ingredients": ["chicken", "spinach", "yogurt", "onions", "garlic"],
            "cooking_time": 35,
            "difficulty": "Medium",
            "category": "Non-Veg"
        },
        {
            "name": "Bhindi Masala",
            "ingredients": ["okra", "tomatoes", "onions", "ginger"],
            "cooking_time": 20,
            "difficulty": "Easy",
            "category": "Veg"
        },
        {
            "name": "Aloo Anda Curry",
            "ingredients": ["eggs", "potatoes", "tomatoes", "onions", "cloves"],
            "cooking_time": 25,
            "difficulty": "Easy",
            "category": "Non-Veg"
        },
        {
            "name": "Egg Fried Rice",
            "ingredients": ["eggs", "rice", "soy sauce", "carrots", "onions"],
            "cooking_time": 15,
            "difficulty": "Easy",
            "category": "Non-Veg"
        },
        {
            "name": "Chicken Karahi",
            "ingredients": ["chicken", "tomatoes", "ginger", "garlic", "green chilies"],
            "cooking_time": 40,
            "difficulty": "Medium",
            "category": "Non-Veg"
        }
    ]
    
    # Score recipes based on available ingredients
    scored_recipes = []
    for recipe in recipe_database:
        # Check for fuzzy matching (if recipe ingredient is a substring of available item or vice versa)
        matching = 0
        for req_ing in recipe["ingredients"]:
            if any(req_ing in avail or avail in req_ing for avail in available_ingredients):
                matching += 1
        
        total = len(recipe["ingredients"])
        
        if matching > 0:
            score = (matching / total) * 100
            scored_recipes.append({
                **recipe,
                "match_percentage": round(score, 1),
                "matching_ingredients": matching,
                "total_ingredients": total
            })
    
    # Sort by match percentage and then difficulty
    scored_recipes.sort(key=lambda x: (x["match_percentage"], -len(x["name"])), reverse=True)
    
    return {
        "suggestions": scored_recipes[:max_results],
        "total_available": len(scored_recipes)
    }


def generate_new_recipe(ingredients: str, preferences: str = ""):
    """
    Generate a completely new Pakistani recipe using AI based on available ingredients
    
    Args:
        ingredients: Comma-separated list of available ingredients
        preferences: Optional preferences (e.g., "vegetarian", "quick", "spicy")
    """
    prompt = f"""
Create a unique Pakistani recipe using these available ingredients: {ingredients}

Preferences: {preferences if preferences else "None"}

Please provide:
1. Recipe Name (in Urdu/English)
2. Ingredients List with quantities
3. Step-by-step cooking instructions (in simple Hinglish)
4. Cooking time
5. Difficulty level (Easy/Medium/Hard)

Make it authentic, practical, and delicious!
"""
    
    try:
        response = client.models.generate_content(
            model='gemini-2.0-flash-exp',
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=1.0,  # More creative
            )
        )
        
        return {
            "success": True,
            "recipe": response.text,
            "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "message": "Could not generate recipe. Please try again."
        }


def mark_meal_cooked(meal_name: str):
    """Mark a meal as cooked today
    
    Args:
        meal_name: Name of the meal that was cooked
    """
    meal = MealHistory.objects.create(
        name=meal_name,
        date_cooked=datetime.now().date()
    )
    
    return {
        "success": True,
        "meal_name": meal.name,
        "date_cooked": meal.date_cooked.strftime("%Y-%m-%d"),
        "message": f"{meal_name} marked as cooked!"
    }
