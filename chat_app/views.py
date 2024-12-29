from rest_framework.viewsets import ModelViewSet
from .models import ChatRoom, ChatRoomParticipant, Message
from .serializers import ChatRoomSerializer, ChatRoomParticipantSerializer, MessageSerializer
from rest_framework.permissions import IsAuthenticated

class ChatRoomViewSet(ModelViewSet):
    queryset = ChatRoom.objects.all()
    serializer_class = ChatRoomSerializer
    permission_classes = [IsAuthenticated]  # Require authentication to access chat rooms


class ChatRoomParticipantViewSet(ModelViewSet):
    queryset = ChatRoomParticipant.objects.all()
    serializer_class = ChatRoomParticipantSerializer
    permission_classes = [IsAuthenticated]  # Require authentication to manage participants


class MessageViewSet(ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]  # Require authentication to manage messages
