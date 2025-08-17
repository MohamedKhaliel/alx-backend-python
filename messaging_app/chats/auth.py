from django.conf import settings
from django.contrib.auth.models import user
from rest_framework import authentication 
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.authentication import JWTAuthentication

class CustomAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        jwt_auth = JWTAuthentication()
        try:
            user, _ = jwt_auth.authenticate(request)
        except AuthenticationFailed:
            return None
        
        if not user or not user.is_active:
            raise AuthenticationFailed('User is inactive or does not exist')
        
        return (user, None)