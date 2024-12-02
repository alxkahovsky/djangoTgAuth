from django.urls import path
from . import views
from .api.router import r

urlpatterns = [
    path('start/', views.auth_start, name='auth_start'),
    path('complete/', views.auth_complete, name='auth_complete'),
]
urlpatterns.extend(r.urls)
