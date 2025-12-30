from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .agent_service import chat_with_agent

class AgentChatView(APIView):
    """
    Chat endpoint for Ammi's AI Assistant.
    Primary entry point for the AI-driven chatbot.
    """
    
    def post(self, request):
        user_message = request.data.get('message', '')
        conversation_history = request.data.get('conversation_history', [])
        
        if not user_message:
            return Response(
                {"error": "Message is required"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            # Call the AI agent which uses Gemini function calling
            result = chat_with_agent(user_message, conversation_history)
            
            return Response({
                "reply": result["message"],
                "conversation_history": result["conversation_history"],
                "error": result.get("error")
            })
            
        except Exception as e:
            return Response(
                {
                    "reply": "Sorry Beta, main thoda thaki hui hoon. Please try again later.",
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
    """Get recent meals for agent history"""
    def get(self, request):
        try:
            days = int(request.query_params.get('days', 3))
        except ValueError:
            days = 3
        from .agent_tools import get_recent_meals
        return Response(get_recent_meals(days))
