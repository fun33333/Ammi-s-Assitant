import os
from google import genai
from google.genai import types
from django.conf import settings
import json

# Ensure we use the correct key
API_KEY = os.getenv('GEMINI_API_KEY', 'AIzaSyDIxFXJWj4VHXLmxCAZP33yd-u9PjwQOCI')
client = genai.Client(api_key=API_KEY)

AGENT_SYSTEM_PROMPT = """
You are Ammi's Recipe Assistant, a warm Pakistani mother figure.
Your goal is to help decide what to cook using Hinglish (Urdu+English).

LOGIC:
- If user asks for suggestions, ALWAYS call suggest_recipes.
- If user asks what they have, call get_current_inventory.
- Always be polite and motherly.
"""

from .agent_tools import (
    get_current_inventory,
    get_recent_meals,
    suggest_recipes,
    mark_meal_cooked,
    generate_new_recipe
)

def chat_with_agent(user_message, conversation_history=None):
    if conversation_history is None:
        conversation_history = []
    
    msg_lower = user_message.lower()

    # --- KEYWORD FALLBACK (If AI is busy/quota error) ---
    # This ensures "Service Issue" doesn't happen for basic stuff
    if any(k in msg_lower for k in ['inventory', 'kya hai', 'samann', 'items']):
        data = get_current_inventory()
        reply = "Beta, aapke paas ye sab hai:\n" + "\n".join([f"• {i['name']} ({i['quantity']})" for i in data['ingredients'][:5]])
        conversation_history.append({'role': 'user', 'content': user_message})
        conversation_history.append({'role': 'model', 'content': reply})
        return {"message": reply, "conversation_history": conversation_history}

    if any(k in msg_lower for k in ['suggest', 'kya pakaon', 'recipe', 'suggestion']):
        data = suggest_recipes()
        if not data['suggestions']:
            reply = "Beta, inventory mein kuch add karo toh main suggest karoon!"
        else:
            reply = "Aaj ye bana lo, achay lagay gain:\n" + "\n".join([f"• {s['name']} ({s['match_percentage']}% Match)" for s in data['suggestions']])
        conversation_history.append({'role': 'user', 'content': user_message})
        conversation_history.append({'role': 'model', 'content': reply})
        return {"message": reply, "conversation_history": conversation_history}

    # --- AI Chat (Gemini) ---
    try:
        contents = []
        for msg in conversation_history[-6:]:
            role = 'user' if msg.get('role') == 'user' else 'model'
            contents.append(types.Content(role=role, parts=[types.Part.from_text(text=msg['content'])]))
        
        contents.append(types.Content(role='user', parts=[types.Part.from_text(text=user_message)]))
        
        response = client.models.generate_content(
            model='gemini-2.0-flash-exp',
            contents=contents,
            config=types.GenerateContentConfig(
                tools=[get_current_inventory, get_recent_meals, suggest_recipes, mark_meal_cooked, generate_new_recipe],
                system_instruction=AGENT_SYSTEM_PROMPT,
                temperature=0.7,
                max_output_tokens=500,
            )
        )
        
        reply_text = response.text
        conversation_history.append({'role': 'user', 'content': user_message})
        conversation_history.append({'role': 'model', 'content': reply_text})
        
        return {"message": reply_text, "conversation_history": conversation_history}
        
    except Exception as e:
        print(f"Gemini Error: {e}")
        # Final fallback if even Gemini fails
        fallback = "Beta, main thoda thaki hui hoon. App please suggestions tab check karle ya ingredients add karein?"
        return {"message": fallback, "conversation_history": conversation_history, "error": str(e)}
