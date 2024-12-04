from django.contrib.auth.backends import BaseBackend
from .models import User
from .jwt_services import jwt_service
import jwt


class SafeJWTAuthentication(BaseBackend):

    def authenticate(self, request, **kwargs):
        queryset = User.objects.filter(is_active=True)
        authorization_header = request.COOKIES.get('_tid')
        if not authorization_header:
            return None
        try:
            access_token = authorization_header
            payload = jwt_service.decode_token(access_token)
        except jwt.ExpiredSignatureError:
            return None
        except Exception as finally_exception:
            return None
        user = queryset.filter(id=payload['user_id']).first()
        if user is None:
            return None
        if not user.is_active:
            return None
        return user
