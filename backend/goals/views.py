from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework import status, permissions
from workflow import ai_engine
from .serializers import GoalSerializer
from .models import Goal
import os
import logging

logger = logging.getLogger(__name__)

class DecomposeGoalView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        raw_input = request.data.get('text')

        if not raw_input:
            return Response(
                {"error": "No text provided"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Initialize workflow with Gemini key
        api_key = os.environ.get('GEMINI_API_KEY')
        workflow = ai_engine.ZimnaWorkflow(api_key=api_key)

        try:
            created_goals = workflow.create_goals_from_ai(request.user, raw_input)

            # Check for clarification error
            if isinstance(created_goals, list) and len(created_goals) > 0:
                if isinstance(created_goals[0], dict) and "error" in created_goals[0]:
                    return Response(created_goals[0], status=status.HTTP_200_OK)

            if not isinstance(created_goals, list):
                created_goals = [created_goals]
            
            serializer = GoalSerializer(created_goals, many=True)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        except Exception as e:
            return Response(
                {"error": "AI Processing Failed", "details": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class GoalListView(ListAPIView):
    """
    Returns a list of all goals and their nested tasks
    for the authenticated user.
    """

    serializer_class = GoalSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Goal.objects.filter(user=self.request.user).prefetch_related('tasks').order_by('-created_at')
    
    def list(self, request, *args, **kwargs):
        try:
            return super().list(request, *args, **kwargs)
        except Exception as e:
            logger.error(f"Error fetching goals for user {request.user.id}: {str(e)}")
            return Response(
                {"error": "Failed to reterieve goals.", "details": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
