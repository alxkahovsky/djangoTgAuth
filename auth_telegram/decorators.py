from functools import wraps
from django.contrib.auth import login
from .auth import SafeJWTAuthentication


def tg_auth_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        auth = SafeJWTAuthentication()
        user = auth.authenticate(request)
        if user is not None:
            login(request, user, backend='auth_telegram.auth.SafeJWTBackend')
            return view_func(request, *args, **kwargs)
        return view_func(request, *args, **kwargs)
    return _wrapped_view
