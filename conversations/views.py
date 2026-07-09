from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import Conversation, Message
from .serializers import MessageSerializer
from .services import handle_yiyara_logic
from goals.models import Goal

class ChatAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        raw_text = request.data.get('content')
        goal_id = request.data.get('goal_id')
        conversation_id = request.data.get('conversation_id')

        if not raw_text:
            return Response({"error": "Message content is required"}, status=status.HTTP_400_BAD_REQUEST)

        # Get or Create the Conversation
        if conversation_id:
            conversation = get_object_or_404(Conversation, id=conversation_id, user=user)
        elif goal_id:
            goal = get_object_or_404(Goal, id=goal_id, user=user)
            conversation, created = Conversation.objects.get_or_create(
                goal=goal, 
                user=user
            )
        else:
            return Response({"error": "Goal ID or Conversation ID required"}, status=status.HTTP_400_BAD_REQUEST)

        # Process logic (Classification -> Action -> Response)
        try:
            ai_message = handle_yiyara_logic(user, conversation, raw_text)
            
            # Return the response with the conversation_id 
            # so the frontend can "lock in" this chat thread
            return Response({
                "conversation_id": conversation.id,
                "message": MessageSerializer(ai_message).data
            }, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ConversationHistoryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, goal_id):
        # 1. Find the conversation for this goal owned by this user
        # We take the latest one created if multiple exist
        conversation = Conversation.objects.filter(
            goal_id=goal_id, 
            user=request.user
        ).order_by('-created_at').first()

        if not conversation:
            # Return an empty list instead of 404 so the frontend doesn't break
            return Response([], status=status.HTTP_200_OK)

        # 2. Get all messages for this conversation
        messages = conversation.messages.all().order_by('created_at')
        serializer = MessageSerializer(messages, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
        