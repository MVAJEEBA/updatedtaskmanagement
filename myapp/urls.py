from django.urls import path
from .views import no_permission

urlpatterns = [
    path('no-permission/', no_permission, name='no_permission'),
]