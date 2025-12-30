from rest_framework.views import APIView
from rest_framework.response import Response
from .agent_tools import suggest_recipes

class DirectSuggestionView(APIView):
    """Direct suggestion endpoint without AI"""
    
    def post(self, request):
        try:
            max_results = request.data.get('max_results', 3)
            suggestions = suggest_recipes(max_results=max_results)
            return Response(suggestions)
        except Exception as e:
            return Response(
                {"error": str(e), "suggestions": []},
                status=500
            )
