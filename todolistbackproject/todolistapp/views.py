from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListAPIView, ListCreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import UserModel, TodoListModel
from .serializers import UserSerializer, LoginSerializer, TodoListSerializer
from rest_framework import permissions, status
from .permissions import IsOwner


class TodolistCreate(ListCreateAPIView):
    serializer_class = TodoListSerializer
    queryset = TodoListModel.objects.all()
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user)

    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)


class TodolistDetail(RetrieveUpdateDestroyAPIView):
    serializer_class = TodoListSerializer
    queryset = TodoListModel.objects.all()
    permission_classes = (IsAuthenticated, IsOwner)
    lookup_field = 'id'

    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user)

    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)


class UserView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = TodoListModel.objects.all()

    def get(self, request, *args, **kwargs):
        example = (
            {
                'id': 0,
                'title': 'Todo 1',
                'completed': 'false'
            },
            {
                'id': 1,
                'title': 'Todo 2',
                'completed': 'False'
            }
        )
        return Response(example)

    def get_queryset(self):
        task = self.request.user.id
        return self.queryset.filter(id=task)
