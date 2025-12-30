import requests
import json

BASE_URL = "http://127.0.0.1:8000/api"

def test_agent_chat():
    print("=== Testing Ammi's AI Agent ===\n")
    
    # Test 1: Simple greeting
    print("1. Testing greeting...")
    response = requests.post(f"{BASE_URL}/agent/chat/", json={
        "message": "Assalam o Alaikum! Aaj khanay mein kya banana hai?"
    })
    
    if response.status_code == 200:
        data = response.json()
        print(f"Agent Reply: {data['reply']}\n")
        conversation = data['conversation_history']
    else:
        print(f"FAILED: {response.status_code} - {response.text}\n")
        return
    
    # Test 2: Ask about ingredients
    print("2. Testing ingredient check...")
    response = requests.post(f"{BASE_URL}/agent/chat/", json={
        "message": "Mere paas kaunse ingredients hain?",
        "conversation_history": conversation
    })
    
    if response.status_code == 200:
        data = response.json()
        print(f"Agent Reply: {data['reply']}\n")
        conversation = data['conversation_history']
    else:
        print(f"FAILED: {response.status_code}\n")
    
    # Test 3: Ask for suggestions
    print("3. Testing recipe suggestions...")
    response = requests.post(f"{BASE_URL}/agent/chat/", json={
        "message": "Koi acha sa recipe suggest karo",
        "conversation_history": conversation
    })
    
    if response.status_code == 200:
        data = response.json()
        print(f"Agent Reply: {data['reply']}\n")
    else:
        print(f"FAILED: {response.status_code}\n")


def test_agent_inventory():
    print("\n=== Testing Inventory API ===\n")
    response = requests.get(f"{BASE_URL}/agent/inventory/")
    if response.status_code == 200:
        data = response.json()
        print(f"Total Ingredients: {data['total_items']}")
        for ing in data['ingredients'][:5]:
            print(f"  - {ing['name']} ({ing['quantity']})")
    else:
        print(f"FAILED: {response.status_code}")


def test_agent_recent_meals():
    print("\n=== Testing Recent Meals API ===\n")
    response = requests.get(f"{BASE_URL}/agent/recent-meals/?days=3")
    if response.status_code == 200:
        data = response.json()
        print(f"Meals in last {data['days_checked']} days: {data['total_meals']}")
        for meal in data['meals']:
            print(f"  - {meal['name']} ({meal['date_cooked']})")
    else:
        print(f"FAILED: {response.status_code}")


if __name__ == "__main__":
    print("⚠️  Note: Make sure to set OPENAI_API_KEY in .env file\n")
    test_agent_inventory()
    test_agent_recent_meals()
    test_agent_chat()
    print("\n=== Tests Complete ===")
