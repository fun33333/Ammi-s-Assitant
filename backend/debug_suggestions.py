import os
import django
import sys

# Setup Django
sys.path.append('d:\\Ammi-s-Assitant\\backend')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ammi_assistant.settings')
django.setup()

from api.agent_tools import suggest_recipes, get_current_inventory

print("--- Current Inventory ---")
inv = get_current_inventory()
print(inv)

print("\n--- Suggestions ---")
sugg = suggest_recipes()
print(sugg)
