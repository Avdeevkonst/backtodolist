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
    permission_classes = (permissions.IsAuthenticated, )

    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user)

    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)


class TodolistDetail(RetrieveUpdateDestroyAPIView):
    serializer_class = TodoListSerializer
    queryset = TodoListModel.objects.all()
    permission_classes = (permissions.IsAuthenticated, IsOwner)
    lookup_field = 'id'

    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user)

    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)


class UserView(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request):
        return Response({'title': 'get request'})

    def post(self, request):
        return Response({'title': 'post request'})
