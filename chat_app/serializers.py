from rest_framework import serializers
from user.serializers import UserSerializer
from .models import ChatRoom, ChatRoomParticipant, Message

class ChatRoomSerializer(serializers.ModelSerializer):
    # participants = UserSerializer(many=True, read_only=True)  # Read-only list of participants

    class Meta:
        model = ChatRoom
        fields = ['id', 'name']  # Expose only these fields


class ChatRoomParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatRoomParticipant
        fields = ['id', 'user', 'room', 'joined_at', 'is_admin']  # Include metadata about the participation


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'room', 'user', 'content', 'timestamp']  # Include all key details of a message
