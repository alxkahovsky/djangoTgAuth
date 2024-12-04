from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie
from .decorators import tg_auth_required


@ensure_csrf_cookie
@tg_auth_required
def auth_page(request):
    if not request.user.is_authenticated:
        return render(request, 'auth_telegram/auth_start.html')
    else:
        return render(request, 'auth_telegram/auth_start.html', {'user': request.user})

