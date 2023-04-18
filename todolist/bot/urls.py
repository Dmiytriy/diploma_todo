from django.urls import path

from todolist.bot import views

urlpatterns = [
    path('verify', views.VerificationView.as_view(), name='verify-bot'),
]
