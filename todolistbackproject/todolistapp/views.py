from django.shortcuts import render
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListAPIView, ListCreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import UserModel, TodoListModel
from .serializers import UserSerializer, LoginSerializer, TodoListSerializer
from rest_framework import permissions
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

    def get(self, request):
        return Response({'title': 'get request'})

    def post(self, request):
        return Response({'title': 'post request'})

    # def get(self, request):
    #     token = request.COOKIES.get('jwt')
    #
    #     if not token:
    #         raise AuthenticationFailed('Unauthenticated!')
    #
    #     try:
    #         payload = jwt.decode(token, 'secret', algorithms=['HS256'])
    #     except jwt.ExpiredSignatureError:
    #         raise AuthenticationFailed('Unauthenticated!')
    #
    #     user = UserModel.objects.filter(id=payload['id']).first()
    #     serializer = UserSerializer(user)
    #     return Response(serializer.data, status=status.HTTP_200_OK)
