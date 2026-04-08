from django.urls import path
from .views import ChatAPIView, ConversationHistoryView

urlpatterns = [
    path('chat/', ChatAPIView.as_view(), name='chat_api'),
    path('history/<uuid:goal_id>/', ConversationHistoryView.as_view(), name='conversation_history'),
]
