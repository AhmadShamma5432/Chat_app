from django.apps import AppConfig
from django.core.management import call_command

class ChatAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'chat_app'

    def ready(self):
        # Call the custom command after apps are loaded
        try:
            call_command('clear_participants')
        except Exception as e:
            print(f"Error running clear_participants command: {e}")
