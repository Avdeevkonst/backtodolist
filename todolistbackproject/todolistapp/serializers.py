from rest_framework import serializers
from .models import UserModel, TodoListModel
from django.contrib import auth
from rest_framework.exceptions import AuthenticationFailed


class TodoListSerializer(serializers.ModelSerializer):

    owner = serializers.ReadOnlyField(source='owner.email')

    class Meta:

        model = TodoListModel
        fields = ('id', 'created', 'title', 'description', 'status', 'owner',)


class UserSerializer(serializers.ModelSerializer):

    tasks = serializers.HyperlinkedRelatedField(many=True, view_name='todo-detail', read_only=True)

    def create(self, validated_data):
        user_instance = UserModel.objects.create_user(**validated_data)
        user_instance.save()
        return user_instance

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            instance.set_password(value) if attr == 'password' else setattr(instance, attr, value)
        instance.save()
        return instance

    class Meta:
        model = UserModel
        fields = ('id', 'email', 'is_ban', 'tasks', 'is_superuser')


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    token = serializers.CharField(read_only=True)

    class Meta:
        model = UserModel
        fields = ('email', 'password', 'token')

    def validate(self, data):
        email = data.get('email', None)
        password = data.get('password', None)
        user = auth.authenticate(email=email, password=password)
        if user.is_ban:
            raise AuthenticationFailed('Account is banned from admin, create new account')
        if not user:
            raise AuthenticationFailed('invalid credentials, try again')
        return {
            'email': user.email,
            'token': user.token
        }


class RegistrationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=50)
    password = serializers.CharField(max_length=150, write_only=True)
    token = serializers.CharField(read_only=True)

    class Meta:
        model = UserModel
        fields = (
            'email', 'password', 'token'
        )

    def create(self, validated_data):
        return UserModel.objects.create_user(**validated_data)


