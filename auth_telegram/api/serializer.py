from ..models import User, TelegramUser, TelegramAuthSession
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .services import generate_password


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['username']


class TelegramUserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')

    class Meta:
        model = TelegramUser
        fields = ('telegram_id', 'username')

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = User.objects.create(**user_data)
        user.set_password(generate_password(10))
        user.save()
        telegram_user = TelegramUser.objects.create(user=user, **validated_data)
        return telegram_user

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', {})
        user = instance.user
        for attr, value in user_data.items():
            setattr(user, attr, value)
        user.save()
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class TelegramAuthSessionSerializer(ModelSerializer):
    id = serializers.CharField(read_only=True)

    class Meta:
        model = TelegramAuthSession
        fields = ['id', 'created']
