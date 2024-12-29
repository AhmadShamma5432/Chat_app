from django.urls import path, include

urlpatterns = [
    path('auth/', include('djoser.urls')),  # User management (registration, password reset)
    path('auth/', include('djoser.urls.jwt')),  # JWT endpoints
]