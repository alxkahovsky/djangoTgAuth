import datetime
import jwt
from django.conf import settings
from rest_framework import exceptions


class JWTService:
    def __init__(self, sercet_key=settings.SECRET_KEY,
                 access_token_ttl=60 * 24 * 3,
                 refresh_token_ttl=60 * 24 * 14):
        self.__secret_key = sercet_key
        self.access_token_ttl = access_token_ttl
        self.refresh_token_ttl = refresh_token_ttl

    def generate_access_token(self, user_id):
        access_token_payload = {
            'user_id': user_id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=self.access_token_ttl),
            'iat': datetime.datetime.utcnow(),
        }
        access_token = jwt.encode(access_token_payload,
                                  self.__secret_key, algorithm='HS256')
        return access_token

    def generate_refresh_token(self, user_id):
        refresh_token_payload = {
            'user_id': user_id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=self.refresh_token_ttl),
            'iat': datetime.datetime.utcnow(),
        }
        access_token = jwt.encode(refresh_token_payload,
                                  self.__secret_key, algorithm='HS256')
        return access_token

    def decode_token(self, token):
        try:
            payload = jwt.decode(
                token, self.__secret_key, algorithms=['HS256'])
            return payload
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed('access_token expired')


jwt_service = JWTService()
