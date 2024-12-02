import uuid

from django.contrib.messages.storage import session
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt


from .models import TelegramUser, User


def generate_token():
    return str(uuid.uuid4())


def auth_start(request):
    token = generate_token()
    request.session[f'{token}'] = {"username": None, "password": None, "telegram_id": None}
    return render(request, 'auth_telegram/auth_start.html', {'token': token})


@csrf_exempt
def auth_complete(request):
    data = request.POST
    try:
        user = User.objects.get_or_create(username=data.get('telegram_username'), password='secretPassword')
        print(user)
        tg_user = TelegramUser.objects.get_or_create(user=user.id, telegram_id=data.get('telegram_id'))
        if tg_user:
            return HttpResponse(200)
        else:
            return HttpResponse(404)
    except Exception as e:
        print(e)
        return HttpResponse(400)
