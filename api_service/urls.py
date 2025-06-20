"""
URL configuration for api_service project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include

from .views import CustomTokenObtainPairView, CustomTokenRefreshView, CustomTokenBlacklistView, CustomUserDeleteView

urlpatterns = [
    # Token endpoints
    path('api/token/blacklist/', CustomTokenBlacklistView.as_view()),
    path('token/refresh/', CustomTokenRefreshView.as_view()),
    path('token/', CustomTokenObtainPairView.as_view()),

    # User delete endpoint
    path('auth/users/delete/', CustomUserDeleteView.as_view()),

    # Djoser endpoints
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),

    # Workout app URLs
    path('workouts/', include('workouts.urls'))
]
