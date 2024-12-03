from django.views.decorators.csrf import csrf_exempt
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import CreateModelMixin, UpdateModelMixin, RetrieveModelMixin
from rest_framework.response import Response
from rest_framework.settings import api_settings
from rest_framework.viewsets import GenericViewSet

from ..jwt_services import jwt_service
from ..models import TelegramUser, TelegramAuthSession
from .serializer import TelegramUserSerializer, TelegramAuthSessionSerializer


class TelegramUserViewSet(RetrieveModelMixin, UpdateModelMixin, CreateModelMixin, GenericViewSet):
    queryset = TelegramUser.objects.all()
    serializer_class = TelegramUserSerializer
    lookup_field = 'telegram_id'
    lookup_url_kwarg = 'telegram_id'



class TelegramAuthSessionViewSet(GenericViewSet):
    queryset = TelegramAuthSession.objects.all()
    serializer_class = TelegramAuthSessionSerializer

    def perform_create(self, serializer):
        serializer.save()

    def get_success_headers(self, data):
        try:
            return {'Location': str(data[api_settings.URL_FIELD_NAME])}
        except (TypeError, KeyError):
            return {}

    @csrf_exempt
    @action(detail=False, methods=['post'])
    def start(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @extend_schema(parameters=[OpenApiParameter(
                name='session_token',
                type=str,
                location=OpenApiParameter.QUERY,
                description='Токен сессии',
                required=True,
            )])
    @action(detail=False, methods=['get'])
    def status(self, request, *args, **kwargs):
        session_token = request.query_params.get('session_token')
        if session_token:
            try:
                auth_session = TelegramAuthSession.objects.get(id=session_token)
                user = TelegramUser.objects.get(session=auth_session)
                token = jwt_service.generate_access_token(user.user.id)
                refresh_token = jwt_service.generate_refresh_token(user.user.id)
                response = Response(status=status.HTTP_302_FOUND)
                response.set_cookie('_tid', token, max_age=3600)  # Устанавливаем куки на 1 час
                response.set_cookie('_trid', refresh_token, max_age=3600*24*14)
                redirect_url = '/'  # Замените на ваш URL
                response['Location'] = redirect_url
                return response
            except Exception as e:
                return Response(status=status.HTTP_400_BAD_REQUEST, data=str(e))

        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)