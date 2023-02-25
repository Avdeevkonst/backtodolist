from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListAPIView, ListCreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import UserModel, TodoListModel
from .serializers import UserSerializer, TodoListSerializer
from rest_framework import permissions, status
from .permissions import IsOwner


class TodolistCreate(ListCreateAPIView):
    serializer_class = TodoListSerializer
    queryset = TodoListModel.objects.all()
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class TodolistDetail(RetrieveUpdateDestroyAPIView):
    serializer_class = TodoListSerializer
    permission_classes = (IsAuthenticated, IsOwner)
    lookup_field = 'id'

    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user)

    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)


class UserTodoView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = TodoListModel.objects.all()
    serializer_class = TodoListSerializer

    def get(self, request, *args, **kwargs):
        objects = TodoListModel.objects.filter(owner__email=self.request.user.email)
        serializer = TodoListSerializer(objects, many=True)
        return Response(status=status.HTTP_200_OK, data=serializer.data)

    def get_queryset(self):
        task = self.request.user.id
        return self.queryset.filter(id=task)
