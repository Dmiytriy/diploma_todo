from typing import Any

from django.contrib.auth import login, logout
from rest_framework import generics, status, permissions
from rest_framework.generics import get_object_or_404
from rest_framework.request import Request
from rest_framework.response import Response

from todolist.core.serializers import CreateUserSerializer, LoginSerializer


class SignUpView(generics.CreateAPIView):
    serializer_class = CreateUserSerializer


class LoginView(generics.CreateAPIView):
    serializer_class = LoginSerializer

    def create(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        login(request=request, user=serializer.save())
        return Response(serializer.data)
