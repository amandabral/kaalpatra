from django.urls import path
from .views import TimeCapsuleAPIView

urlpatterns = [
    path('capsule/', TimeCapsuleAPIView.as_view(), name='time-capsule'),
]