from django.urls import path
from . import views

urlpatterns = [
    path('', views.auth_page, name='auth_page'),
]

