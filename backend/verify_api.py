import requests
import json

BASE_URL = "http://127.0.0.1:8000/api"

def test_full_flow():
    print("--- Starting Full Flow Test ---")
    
    # 1. POST (Create)
    print("\n1. Testing POST (Create)...")
    data = {
        "name": "Test Onion",
        "quantity": "5 kg",
        "expiry_date": "2025-02-20",
        "category": "Vegetable"
    }
    item_id = None
    try:
        response = requests.post(f"{BASE_URL}/ingredients/", json=data)
        if response.status_code == 201:
            item_id = response.json()['id']
            print(f"SUCCESS: Created item with ID {item_id}")
        else:
            print("FAILED POST:", response.text)
            return
    except Exception as e:
        print("ERROR POST:", e)
        return

    # 2. GET (Fetch All)
    print("\n2. Testing GET (Fetch All)...")
    try:
        response = requests.get(f"{BASE_URL}/ingredients/")
        if response.status_code == 200:
            print(f"SUCCESS: Fetched {len(response.json())} items")
        else:
            print("FAILED GET:", response.text)
    except Exception as e:
        print("ERROR GET:", e)

    if not item_id:
        return

    # 3. GET (Fetch Single)
    print(f"\n3. Testing GET (Fetch Single ID: {item_id})...")
    try:
        response = requests.get(f"{BASE_URL}/ingredients/{item_id}/")
        if response.status_code == 200:
            print("SUCCESS: Fetched single item")
        else:
            print("FAILED GET Single:", response.text)
    except Exception as e:
        print("ERROR GET Single:", e)

    # 4. PUT (Update)
    print(f"\n4. Testing PUT (Update ID: {item_id})...")
    update_data = {
        "name": "Updated Onion",
        "quantity": "2 kg",
        "expiry_date": "2025-02-25",
        "category": "Vegetable"
    }
    try:
        response = requests.put(f"{BASE_URL}/ingredients/{item_id}/", json=update_data)
        if response.status_code == 200:
            print("SUCCESS: Updated item", response.json())
        else:
            print("FAILED PUT:", response.text)
    except Exception as e:
        print("ERROR PUT:", e)

    # 5. DELETE
    print(f"\n5. Testing DELETE (ID: {item_id})...")
    try:
        response = requests.delete(f"{BASE_URL}/ingredients/{item_id}/")
        if response.status_code == 204:
            print("SUCCESS: Deleted item")
        else:
            print("FAILED DELETE:", response.text)
    except Exception as e:
        print("ERROR DELETE:", e)

if __name__ == "__main__":
    test_full_flow()
