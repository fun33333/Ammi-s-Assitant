from datetime import datetime, timedelta
from django.db.models import Count, Q
from .models import Ingredient, Recipe, RecipeIngredient, MealHistory

def get_meal_suggestions(preferences=None):
    """
    Get meal suggestions based on available ingredients and preferences.
    
    Args:
        preferences (dict): Optional dict with keys: time, spice_level, diet_type
    
    Returns:
        list: Ranked list of recipes with scores and details
    """
    if preferences is None:
        preferences = {}
    
    # Get all available ingredients
    available_ingredients = set(Ingredient.objects.values_list('name', flat=True))
    
    # Get recipes cooked in last 3 days (to avoid repetition)
    three_days_ago = datetime.now().date() - timedelta(days=3)
    recent_recipes = set(
        MealHistory.objects.filter(date_cooked__gte=three_days_ago)
        .values_list('recipe_id', flat=True)
    )
    
    # Get all recipes
    recipes = Recipe.objects.prefetch_related('recipe_ingredients__ingredient').all()
    
    # Filter by preferences
    if preferences.get('time'):
        recipes = recipes.filter(cooking_time__lte=preferences['time'])
    if preferences.get('spice_level'):
        recipes = recipes.filter(spice_level=preferences['spice_level'])
    if preferences.get('diet_type'):
        recipes = recipes.filter(diet_type=preferences['diet_type'])
    
    # Score each recipe
    scored_recipes = []
    
    for recipe in recipes:
        # Skip recently cooked recipes
        if recipe.id in recent_recipes:
            continue
        
        # Get required ingredients
        recipe_ingredients = recipe.recipe_ingredients.all()
        total_ingredients = recipe_ingredients.count()
        
        if total_ingredients == 0:
            continue
        
        # Count matching ingredients
        matching_count = 0
        missing_ingredients = []
        
        for recipe_ing in recipe_ingredients:
            if recipe_ing.ingredient.name in available_ingredients:
                matching_count += 1
            else:
                missing_ingredients.append(recipe_ing.ingredient.name)
        
        # Calculate base score (percentage match)
        base_score = (matching_count / total_ingredients) * 100
        
        # Bonus for expiry prioritization
        expiry_bonus = 0
        for recipe_ing in recipe_ingredients:
            try:
                ingredient = Ingredient.objects.get(name=recipe_ing.ingredient.name)
                if ingredient.expiry_date:
                    days_to_expiry = (ingredient.expiry_date - datetime.now().date()).days
                    if 0 < days_to_expiry <= 3:
                        expiry_bonus += 20  # High bonus for near expiry
                    elif 3 < days_to_expiry <= 7:
                        expiry_bonus += 10  # Medium bonus
            except Ingredient.DoesNotExist:
                pass
        
        # Final score
        final_score = base_score + expiry_bonus
        
        scored_recipes.append({
            'recipe': recipe,
            'score': round(final_score, 2),
            'match_percentage': round(base_score, 2),
            'missing_ingredients': missing_ingredients,
            'expiry_bonus': expiry_bonus
        })
    
    # Sort by score and return top 5
    scored_recipes.sort(key=lambda x: x['score'], reverse=True)
    return scored_recipes[:5]
