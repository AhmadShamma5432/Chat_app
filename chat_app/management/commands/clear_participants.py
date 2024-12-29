from django.core.management.base import BaseCommand
from chat_app.models import ChatRoomParticipant

class Command(BaseCommand):
    help = 'Clear all ChatRoomParticipant entries'

    def handle(self, *args, **kwargs):
        try:
            ChatRoomParticipant.objects.all().delete()
            self.stdout.write(self.style.SUCCESS('Successfully cleared all ChatRoomParticipant entries.'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error clearing participants: {e}'))
