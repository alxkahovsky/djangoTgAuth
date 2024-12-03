from django.contrib.auth.backends import BaseBackend
from rest_framework.authentication import BaseAuthentication
from .models import User
from .jwt_services import jwt_service
import jwt
from rest_framework import exceptions


class SafeJWTAuthentication(BaseBackend):
    # def authenticate2(self, request):
    #     queryset = User.objects.filter(is_active=True)
    #     authorization_header = request.COOKIES.get('refreshtoken')
    #     if not authorization_header:
    #         return None
    #     try:
    #         access_token = authorization_header
    #         payload = jwt_service.decode_token(access_token)
    #     except jwt.ExpiredSignatureError:
    #         raise exceptions.AuthenticationFailed('refresh_token expired')
    #     except Exception as finally_exception:
    #         raise exceptions.AuthenticationFailed(finally_exception)
    #     user = queryset.objects.filter(id=payload['user_id']).first()
    #     if user is None:
    #         raise exceptions.AuthenticationFailed('User not found')
    #     if not user.is_active:
    #         raise exceptions.AuthenticationFailed('User is inactive or deleted')
    #     return user, None

    def authenticate(self, request, username=None, password=None, **kwargs):
        queryset = User.objects.filter(is_active=True)
        authorization_header = request.COOKIES.get('refreshtoken')
        if not authorization_header:
            return None
        try:
            access_token = authorization_header
            payload = jwt_service.decode_token(access_token)
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed('refresh_token expired')
        except Exception as finally_exception:
            raise exceptions.AuthenticationFailed(finally_exception)
        user = queryset.objects.filter(id=payload['user_id']).first()
        if user is None:
            raise exceptions.AuthenticationFailed('User not found')
        if not user.is_active:
            raise exceptions.AuthenticationFailed('User is inactive or deleted')
        return user
