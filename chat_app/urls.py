from rest_framework.routers import DefaultRouter
from .views import ChatRoomViewSet, ChatRoomParticipantViewSet, MessageViewSet

router = DefaultRouter()
router.register('chatrooms', ChatRoomViewSet, basename='chatroom')
router.register('participants', ChatRoomParticipantViewSet, basename='participant')
router.register('messages', MessageViewSet, basename='message')

urlpatterns = router.urls  # Expose the routes
