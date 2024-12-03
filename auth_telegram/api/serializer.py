from django.db import transaction

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
    session = serializers.CharField(write_only=True, source='session.id')

    class Meta:
        model = TelegramUser
        fields = ('telegram_id', 'username', 'session')

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        with transaction.atomic():
            user = User.objects.create(**user_data)
            auth_session = TelegramAuthSession.objects.get(**validated_data['session'])
            validated_data.pop('session')
            user.set_password(generate_password(10))
            user.save()
            telegram_user = TelegramUser.objects.create(user=user, session=auth_session, **validated_data)
        return telegram_user

    # ToDo отрефакторить сохранение объектоав БД
    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', {})
        user = instance.user
        for attr, value in user_data.items():
            setattr(user, attr, value)
        user.save()
        auth_session = TelegramAuthSession.objects.get(**validated_data['session'])
        validated_data.pop('session')
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.session = auth_session
        instance.save()
        return instance


class TelegramAuthSessionSerializer(ModelSerializer):
    id = serializers.CharField(read_only=True)

    class Meta:
        model = TelegramAuthSession
        fields = ['id', 'created']
