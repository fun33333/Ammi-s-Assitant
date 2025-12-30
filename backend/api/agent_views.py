from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .agent_service import chat_with_agent
from .agent_tools import get_current_inventory, get_recent_meals, suggest_recipes

class AgentChatView(APIView):
    """
    Chat endpoint for Ammi's AI Assistant with fallback for common queries
    """
    
    def post(self, request):
        user_message = request.data.get('message', '')
        conversation_history = request.data.get('conversation_history', [])
        
        if not user_message:
            return Response(
                {"error": "Message is required"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Simple keyword-based fallback for common queries
        message_lower = user_message.lower()
        
        try:
            # Check for simple queries that don't need AI
            if any(word in message_lower for word in ['inventory', 'ingredients', 'what do i have', 'kya hai']):
                inventory = get_current_inventory()
                reply = f"Here's what you have:\n\n"
                for ing in inventory['ingredients'][:5]:
                    urgency = f" (⚠️ {ing.get('urgency', 'fresh')})" if ing.get('urgency') else ""
                    reply += f"• {ing['name']} - {ing['quantity']}{urgency}\n"
                reply += f"\nTotal: {inventory['total_items']} items"
                
                conversation_history.append({'role': 'user', 'content': user_message})
                conversation_history.append({'role': 'model', 'content': reply})
                
                return Response({
                    "reply": reply,
                    "conversation_history": conversation_history
                })
            
            elif any(word in message_lower for word in ['suggest', 'recipe', 'cook', 'banana', 'kya banao']):
                suggestions = suggest_recipes(max_results=3)
                reply = "Here are some recipe suggestions:\n\n"
                for i, recipe in enumerate(suggestions['suggestions'], 1):
                    reply += f"{i}. **{recipe['name']}** ({recipe['cooking_time']} mins)\n"
                    reply += f"   Match: {recipe['match_percentage']}% | Difficulty: {recipe['difficulty']}\n\n"
                
                conversation_history.append({'role': 'user', 'content': user_message})
                conversation_history.append({'role': 'model', 'content': reply})
                
                return Response({
                    "reply": reply,
                    "conversation_history": conversation_history
                })
            
            elif any(word in message_lower for word in ['recent', 'history', 'cooked', 'banaya']):
                meals = get_recent_meals(days=3)
                if meals['total_meals'] == 0:
                    reply = "No meals recorded in the last 3 days. Start cooking! 👨‍🍳"
                else:
                    reply = f"Recent meals (last 3 days):\n\n"
                    for meal in meals['meals']:
                        reply += f"• {meal['name']} ({meal['date_cooked']})\n"
                
                conversation_history.append({'role': 'user', 'content': user_message})
                conversation_history.append({'role': 'model', 'content': reply})
                
                return Response({
                    "reply": reply,
                    "conversation_history": conversation_history
                })
            
            # For complex queries, use AI
            result = chat_with_agent(user_message, conversation_history)
            
            return Response({
                "reply": result["message"],
                "conversation_history": result["conversation_history"],
                "error": result.get("error")
            })
            
        except Exception as e:
            return Response(
                {
                    "reply": "Sorry, I'm having trouble right now. Try asking about your inventory or for recipe suggestions!",
                    "error": str(e)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class AgentInventoryView(APIView):
    """Get current inventory for agent"""
    
    def get(self, request):
        from .agent_tools import get_current_inventory
        return Response(get_current_inventory())


class AgentRecentMealsView(APIView):
    """Get recent meals for agent"""
    
    def get(self, request):
        days = int(request.query_params.get('days', 3))
        from .agent_tools import get_recent_meals
        return Response(get_recent_meals(days))
