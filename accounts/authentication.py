from rest_framework_simplejwt.authentication import JWTAuthentication


class CustomJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        print(f"AUTH CHECK - Cookies: {request.COOKIES}")
        print(f"AUTH CHECK - Headers: {dict(request.headers)}")
        print(f"AUTH CHECK - Path: {request.path}")

        access_token = request.COOKIES.get("access")
        
        if access_token is None:
            print("AUTH CHECK - No access token found in cookies")
            return None
        
        print(f"AUTH CHECK - Found access token: {access_token[:20]}")
        
        validated_token = self.get_validated_token(access_token)

        return self.get_user(validated_token), validated_token