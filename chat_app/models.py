from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()  # Dynamically fetch the User model


class ChatRoom(models.Model):
    name = models.CharField(max_length=255, unique=True)  # Unique room name

    def __str__(self):
        return self.name


class ChatRoomParticipant(models.Model):
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name="chatroom_participations"  # User's participation in chat rooms
    )
    room = models.ForeignKey(
        ChatRoom, 
        on_delete=models.CASCADE, 
        related_name="participants"  # Participants of a specific chat room
    )
    joined_at = models.DateTimeField(auto_now_add=True)  # When the user joined the room
    is_admin = models.BooleanField(default=False)  # Role of the participant

    class Meta:
        unique_together = ('user', 'room')  # Prevent duplicate entries

    def __str__(self):
        return f"{self.user.username} in {self.room.name}"


class Message(models.Model):
    room = models.ForeignKey(
        ChatRoom, 
        on_delete=models.CASCADE, 
        related_name="messages"  # Messages in a specific room
    )
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name="messages"  # Messages sent by a specific user
    )
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)  # Automatically set on creation

    def __str__(self):
        return f"{self.user.username} in {self.room.name}: {self.content[:20]}"
