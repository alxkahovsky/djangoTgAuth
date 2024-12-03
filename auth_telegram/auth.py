from django.contrib.auth.backends import BaseBackend
from rest_framework.authentication import BaseAuthentication
from .models import User
from .jwt_services import jwt_service
import jwt
from rest_framework import exceptions


class SafeJWTAuthentication(BaseBackend):

    def authenticate(self, request, username=None, password=None, **kwargs):
        queryset = User.objects.filter(is_active=True)
        authorization_header = request.COOKIES.get('_tid')
        print(authorization_header)
        if not authorization_header:
            return None
        try:
            access_token = authorization_header
            print(access_token)
            payload = jwt_service.decode_token(access_token)
            print(payload)
        except jwt.ExpiredSignatureError:
            return None
        except Exception as finally_exception:
            return None
        user = queryset.filter(id=payload['user_id']).first()
        if user is None:
            return None
        if not user.is_active:
            return None
        print(f'user: {user}')

        return user
