# chat_app/signals.py
from django.core.signals import request_started
from django.dispatch import receiver
from chat_app.models import ChatRoomParticipant

@receiver(request_started)
def clear_stale_participants(sender, **kwargs):
    try:
        ChatRoomParticipant.objects.all().delete()
        print("Cleared all ChatRoomParticipant entries.")
    except Exception as e:
        print(f"Error while clearing participants: {e}")
