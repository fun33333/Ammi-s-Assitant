import requests
import json

BASE_URL = "http://127.0.0.1:8000/api"

def test_recipes():
    print("=== Testing Recipe APIs ===\n")
    
    # Get all recipes
    print("1. GET all recipes...")
    response = requests.get(f"{BASE_URL}/recipes/")
    if response.status_code == 200:
        recipes = response.json()
        print(f"SUCCESS: Found {len(recipes)} recipes")
        if recipes:
            print(f"Sample recipe: {recipes[0]['name']}")
    else:
        print(f"FAILED: {response.status_code}")

def test_suggestions():
    print("\n=== Testing Meal Suggestion API ===\n")
    
    # Test 1: No preferences
    print("1. Testing with no preferences...")
    response = requests.post(f"{BASE_URL}/suggestions/", json={})
    if response.status_code == 200:
        data = response.json()
        print(f"SUCCESS: Got {data['count']} suggestions")
        for i, suggestion in enumerate(data['suggestions'][:3], 1):
            print(f"  {i}. {suggestion['recipe']['name']} (Score: {suggestion['score']}, Match: {suggestion['match_percentage']}%)")
            if suggestion['missing_ingredients']:
                print(f"     Missing: {', '.join(suggestion['missing_ingredients'][:3])}")
    else:
        print(f"FAILED: {response.status_code} - {response.text}")
    
    # Test 2: With time preference
    print("\n2. Testing with time preference (max 30 mins)...")
    response = requests.post(f"{BASE_URL}/suggestions/", json={"time": 30})
    if response.status_code == 200:
        data = response.json()
        print(f"SUCCESS: Got {data['count']} quick recipes")
        for i, suggestion in enumerate(data['suggestions'], 1):
            print(f"  {i}. {suggestion['recipe']['name']} ({suggestion['recipe']['cooking_time']} mins)")
    else:
        print(f"FAILED: {response.status_code}")
    
    # Test 3: With diet preference
    print("\n3. Testing with diet preference (Veg)...")
    response = requests.post(f"{BASE_URL}/suggestions/", json={"diet_type": "Veg"})
    if response.status_code == 200:
        data = response.json()
        print(f"SUCCESS: Got {data['count']} vegetarian recipes")
        for i, suggestion in enumerate(data['suggestions'], 1):
            print(f"  {i}. {suggestion['recipe']['name']}")
    else:
        print(f"FAILED: {response.status_code}")

def test_mark_as_cooked():
    print("\n=== Testing Mark as Cooked ===\n")
    
    # Get a recipe ID first
    response = requests.get(f"{BASE_URL}/recipes/")
    if response.status_code == 200:
        recipes = response.json()
        if recipes:
            recipe_id = recipes[0]['id']
            recipe_name = recipes[0]['name']
            
            # Mark as cooked
            print(f"Marking '{recipe_name}' as cooked...")
            response = requests.post(f"{BASE_URL}/history/", json={
                "recipe": recipe_id,
                "name": recipe_name
            })
            if response.status_code == 201:
                print("SUCCESS: Recipe marked as cooked")
                
                # Verify it's excluded from next suggestion
                print("\nVerifying repetition prevention...")
                response = requests.post(f"{BASE_URL}/suggestions/", json={})
                if response.status_code == 200:
                    data = response.json()
                    suggested_names = [s['recipe']['name'] for s in data['suggestions']]
                    if recipe_name not in suggested_names:
                        print(f"✅ SUCCESS: '{recipe_name}' is excluded from suggestions")
                    else:
                        print(f"⚠ WARNING: '{recipe_name}' still in suggestions")
            else:
                print(f"FAILED: {response.status_code}")

if __name__ == "__main__":
    test_recipes()
    test_suggestions()
    test_mark_as_cooked()
    print("\n=== All Tests Complete ===")
