import jwt
from django.conf import settings
from channels.middleware import BaseMiddleware
from asgiref.sync import sync_to_async

class JwtAuthMiddleware(BaseMiddleware):
    """
    Custom WebSocket middleware for authenticating users via JWT from headers.
    """
    async def __call__(self, scope, receive, send):
        from django.contrib.auth.models import AnonymousUser  # Delayed import inside method

        # Extract token from headers
        token = self.get_token_from_headers(scope.get("headers", []))
        
        # Decode token and attach user to scope
        scope["user"] = await self.get_user_from_token(token) if token else AnonymousUser()
        return await super().__call__(scope, receive, send)

    def get_token_from_headers(self, headers):
        """
        Extract the JWT token from the headers.
        """
        for header_name, header_value in headers:
            if header_name == b"authorization":  # Check for the Authorization header
                header_value = header_value.decode("utf-8")  # Decode bytes to string
                if header_value.startswith("JWT "):  # Ensure the header uses the correct format
                    return header_value.split("JWT ")[1]
        return None

    @sync_to_async
    def get_user_from_token(self, token):
        """
        Decode the JWT token and retrieve the associated user.
        """
        from django.contrib.auth import get_user_model  # Delayed import inside method
        User = get_user_model()  # Fetch model after apps are ready

        try:
            # Decode JWT token
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            user_id = payload.get("user_id")
            # Fetch the user from the database
            return User.objects.get(id=user_id)
        except (jwt.ExpiredSignatureError, jwt.DecodeError, User.DoesNotExist):
            from django.contrib.auth.models import AnonymousUser
            return AnonymousUser()


class ClearStaleParticipantsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.has_cleared = False  # Ensure the cleanup runs only once

    def __call__(self, request):
        from chat_app.models import ChatRoomParticipant
        if not self.has_cleared:
            try:
                ChatRoomParticipant.objects.all().delete()
                print("Successfully cleared ChatRoomParticipant entries.")
                self.has_cleared = True
            except Exception as e:
                print(f"Error clearing participants: {e}")
        return self.get_response(request)
