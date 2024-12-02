from ..models import User, TelegramUser
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers


def generate_password():
    return 'NewPasswordForUser'


class UserSerializer(ModelSerializer):
    password = serializers.CharField(required=False, allow_null=True, write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password']


class TelegramUserSerializer(ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = TelegramUser
        fields = '__all__'