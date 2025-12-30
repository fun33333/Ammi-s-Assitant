import os
from google import genai
from google.genai import types
from django.conf import settings
import json

# Initialize Gemini client
client = genai.Client(api_key=os.getenv('GEMINI_API_KEY', 'AIzaSyBw4XnFJAVp78yIqAIspeLMhsXnJEC-gqw'))

AGENT_SYSTEM_PROMPT = """
You are Ammi's Recipe Assistant, helping Pakistani families decide what to cook.

Your personality:
- Warm and encouraging like a helpful Ammi
- Use simple Urdu/English mix naturally (Hinglish)
- Suggest practical Pakistani recipes
- Consider available ingredients, expiry dates, and recent meals

Your capabilities:
1. Check current ingredient inventory
2. View meal history to avoid repetition
3. Suggest recipes based on available ingredients
4. Provide step-by-step cooking instructions
5. Generate new recipes when needed

Always prioritize:
- Using ingredients near expiry
- Avoiding recently cooked meals (last 3 days)
- Practical, easy-to-follow recipes
- Encouraging and friendly tone

When greeting, use phrases like:
- "Aaj khanay mein kya banana hai?"
- "Kya ingredients hain ghar mein?"
- "Main aapki madad karoon?"

IMPORTANT: Keep responses concise and friendly. Use bullet points for recipes.
"""


# Tool functions (imported from agent_tools.py)
from .agent_tools import (
    get_current_inventory,
    get_recent_meals,
    suggest_recipes,
    mark_meal_cooked,
    generate_new_recipe
)


def chat_with_agent(user_message, conversation_history=None):
    """
    Main function to chat with the Gemini AI agent
    
    Args:
        user_message (str): User's message
        conversation_history (list): Previous messages in conversation
    
    Returns:
        dict: Agent's response and updated conversation history
    """
    if conversation_history is None:
        conversation_history = []
    
    # Build conversation contents for Gemini
    contents = []
    
    # Add previous conversation (limit to last 10 messages to avoid quota issues)
    recent_history = conversation_history[-10:] if len(conversation_history) > 10 else conversation_history
    for msg in recent_history:
        if msg.get('role') == 'user':
            contents.append(msg['content'])
        elif msg.get('role') == 'model':
            contents.append(msg['content'])
    
    # Add current user message
    contents.append(user_message)
    
    # Call Gemini API with automatic function calling
    try:
        response = client.models.generate_content(
            model='gemini-2.0-flash-exp',
            contents=contents,
            config=types.GenerateContentConfig(
                tools=[
                    get_current_inventory,
                    get_recent_meals,
                    suggest_recipes,
                    mark_meal_cooked,
                    generate_new_recipe
                ],
                system_instruction=AGENT_SYSTEM_PROMPT,
                temperature=0.7,
                max_output_tokens=500,  # Limit to reduce quota usage
            )
        )
        
        # Get response text
        assistant_message = response.text
        
        # Update conversation history
        conversation_history.append({
            'role': 'user',
            'content': user_message
        })
        conversation_history.append({
            'role': 'model',
            'content': assistant_message
        })
        
        return {
            "message": assistant_message,
            "conversation_history": conversation_history
        }
    
    except Exception as e:
        error_str = str(e)
        
        # Handle quota errors gracefully
        if "quota" in error_str.lower() or "429" in error_str:
            fallback_message = "Sorry, I'm experiencing high demand right now. Let me help you with a simple suggestion: Try checking your inventory and I can suggest recipes based on what you have!"
        else:
            fallback_message = f"Sorry, I encountered an error. Please try again or ask me to check your inventory."
        
        conversation_history.append({
            'role': 'user',
            'content': user_message
        })
        conversation_history.append({
            'role': 'model',
            'content': fallback_message
        })
        
        return {
            "message": fallback_message,
            "conversation_history": conversation_history,
            "error": error_str
        }
