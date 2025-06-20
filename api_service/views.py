from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView, TokenBlacklistView
)
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import status
from datetime import timedelta
from django.contrib.auth import get_user_model
from django.conf import settings
from datetime import datetime, timedelta
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated


User = get_user_model()

class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request):
        try:
            response = super().post(request)

            access_token = response.data.get('access')
            refresh_token = response.data.get('refresh')

            secure_cookie = settings.ENVIRONMENT == 'production'
            samesite = 'None' if settings.ENVIRONMENT == 'production' else 'Lax'

            access_expires = datetime.now() + timedelta(minutes=5)
            refresh_expires = datetime.now() + timedelta(days=1)

            # Set access and refresh cookies
            response.set_cookie('access', access_token, httponly=True, secure=secure_cookie, samesite=samesite, expires=access_expires)
            response.set_cookie('refresh', refresh_token, httponly=True, secure=secure_cookie, samesite=samesite, expires=refresh_expires)
            response.data = {}
            
            return response
        except Exception as e:
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

            response = Response(status=status.HTTP_200_OK)

            secure_cookie = settings.ENVIRONMENT == 'production'
            samesite = 'None' if settings.ENVIRONMENT == 'production' else 'Lax'
            access_expires = datetime.now() + timedelta(minutes=5)
            refresh_expires = datetime.now() + timedelta(days=1)
    
            response.set_cookie("access", str(new_access),  httponly=True, secure=secure_cookie, samesite=samesite, expires=access_expires)
            response.set_cookie("refresh", str(new_refresh),  httponly=True, secure=secure_cookie, samesite=samesite, expires=refresh_expires)

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

            response = Response({"details": "Logged out successfully."})

            if settings.ENVIRONMENT == 'production':
                past_date = datetime.now() - timedelta(seconds=1)
                
                if access:
                    response.set_cookie(
                        "access", 
                        "", 
                        expires=past_date,
                        httponly=True,
                        secure=True,
                        samesite='None'
                    )

                response.set_cookie(
                    "refresh",
                    "",
                    expires=past_date,
                    httponly=True,
                    secure=True,
                    samesite='None'
                )
            else:
                if access:
                    response.delete_cookie("access")
                response.delete_cookie("refresh")

            return response

        except Exception as e:
            return Response({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
        

class CustomUserDeleteView(APIView):
    permission_classes = [IsAuthenticated]
    
    def delete(self, request):
        refresh_cookie = request.COOKIES.get("refresh")
        access_cookie = request.COOKIES.get("access")
        
        # Blacklist refresh token if it exists
        if refresh_cookie:
            try:
                refresh_token = RefreshToken(refresh_cookie)
                refresh_token.blacklist()
            except Exception:
                # Continue with deletion if token is already blacklisted
                pass
        
        # Delete the user
        user = request.user
        user.delete()
        
        response = Response(status=status.HTTP_204_NO_CONTENT)
        
        # Clear cookies
        if settings.ENVIRONMENT == 'production':
            past_date = datetime.now() - timedelta(seconds=1)
            
            if access_cookie:
                response.set_cookie(
                    "access", 
                    "", 
                    expires=past_date,
                    httponly=True,
                    secure=True,
                    samesite='None'
                )

            if refresh_cookie:
                response.set_cookie(
                    "refresh",
                    "",
                    expires=past_date,
                    httponly=True,
                    secure=True,
                    samesite='None'
                )
        else:
            if access_cookie:
                response.delete_cookie("access")
            if refresh_cookie:
                response.delete_cookie("refresh")
        
        return response