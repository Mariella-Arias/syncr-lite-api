from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView, TokenBlacklistView
)
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import status
from datetime import timedelta
from django.contrib.auth import get_user_model

User = get_user_model()

class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request):
        try:
            response = super().post(request)

            access_token = response.data.get('access')
            refresh_token = response.data.get('refresh')

            # Set access and refresh cookies
            # TODO: set secure=True in production
            response.set_cookie('access', access_token, httponly=True, secure=False, samesite='None', max_age=timedelta(minutes=5))
            response.set_cookie('refresh', refresh_token, httponly=True, secure=False, samesite='None', max_age=timedelta(days=1))
            response.data = {}
            
            return response
        except:
           return Response({"detail" : "Invalid credentials."}, status=status.HTTP_401_UNAUTHORIZED)

class CustomTokenRefreshView(TokenRefreshView):
    def post(self, request):
        refresh = request.COOKIES.get("refresh")

        if not refresh:
            return Response({"detail": "Refresh token not provided."}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            old_refresh = RefreshToken(refresh)
            
            old_refresh.blacklist()
           
            user = old_refresh.payload['user_id']
    
            new_refresh = RefreshToken.for_user(User.objects.get(pk=user))
            new_access = new_refresh.access_token

            response = Response({"access": str(new_access), "refresh": str(new_refresh)}, status=status.HTTP_200_OK)

            response.set_cookie("refresh", str(new_refresh),  httponly=True, secure=False, samesite='None', max_age=timedelta(days=1))
            response.set_cookie("access", str(new_access),  httponly=True, secure=False, samesite='None', max_age=timedelta(minutes=5))
        
            return response
    
        except Exception as e:
            return Response({"detail":str(e)}, status=status.HTTP_401_UNAUTHORIZED)
        
class CustomTokenBlacklistView(TokenBlacklistView):
    def post(self, request):
        refresh = request.COOKIES.get("refresh")
        access = request.COOKIES.get("access")

        if not refresh:
            return Response({"details": "Refresh token not provided."}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            refresh_token = RefreshToken(refresh)
            refresh_token.blacklist()

            if access:
                response = Response({"details": "Logged out successfully."})
                response.delete_cookie("access")
                response.delete_cookie("refresh")

                return response
            
            response = Response({"details": "Logged out successfully."})
            response.delete_cookie("refresh")

            return response

        except:
            return Response({"detail" : "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
