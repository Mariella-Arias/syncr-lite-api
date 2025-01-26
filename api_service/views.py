from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import status
from datetime import timedelta

class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request):
        try:
            response = super().post(request)

            access_token = response.data.get('access')
            refresh_token = response.data.get('refresh')

            # Set access and refresh cookies
            # TODO: set secure=True in production
            response.set_cookie('access', access_token, httponly=True, secure=False, samesite='None', max_age=timedelta(minutes=2))
            response.set_cookie('refresh', refresh_token, httponly=True, secure=False, samesite='None', max_age=timedelta(days=1))
            response.data = {}
            
            return response
        except:
           return Response({"detail" : "Invalid credentials."}, status=status.HTTP_401_UNAUTHORIZED)


class CustomTokenRefreshView(TokenRefreshView):
    def post(self, request):
        refresh_token = request.COOKIES.get("refresh")

        if not refresh_token:
            return Response({"detail": "Refresh token not provided."}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            fresh_token = RefreshToken(refresh_token)

            # Set new access cookie
            response = Response({"access": str(fresh_token.access_token)})
            response.set_cookie("access", str(fresh_token.access_token),  httponly=True, secure=False, samesite='None', max_age=timedelta(minutes=5))
            return response
    
        except Exception as e:
            return Response({"detail":str(e)}, status=status.HTTP_401_UNAUTHORIZED)