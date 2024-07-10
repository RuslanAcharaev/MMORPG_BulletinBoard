from django.urls import path
from .views import ConfirmEmailView

urlpatterns = [
    path('confirm/', ConfirmEmailView.as_view(), name='confirm'),
]
