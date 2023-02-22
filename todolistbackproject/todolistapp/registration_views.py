import datetime
import jwt
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework.views import APIView
from .renderers import UserJSONRenderer
from .models import UserModel
from .serializers import UserSerializer, LoginSerializer, RegistrationSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework import permissions
from rest_framework.generics import RetrieveUpdateAPIView, GenericAPIView


class UserAuthenticationView(GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = (permissions.AllowAny,)
    renderer_classes = (UserJSONRenderer, )

    def post(self, request):
        # email = request.data['email']
        # password = request.data['password']

        # user = UserModel.objects.filter(email=email).first()
        # if not user.check_password(password):
        #     raise AuthenticationFailed('Incorrect password!')

        # if user.is_ban:
        #     return Response({'errors': 'The requested user is banned'}, status=status.HTTP_400_BAD_REQUEST)
        #
        # if not user.is_active:
        #     return Response({'errors': 'User is not active'})
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

        # payload = {
        #     'id': user.id,
        #     'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
        #     'iat': datetime.datetime.utcnow()
        # }
        #
        # token = jwt.encode(payload, 'secret', algorithm='HS256')
        #
        # response = Response()
        #
        # response.set_cookie(key='jwt', value=token, httponly=True)
        # response.data = {
        #     'jwt': token
        # }
        # return response


class UserRegistrationView(APIView):
    serializer_class = RegistrationSerializer
    renderer_classes = (UserJSONRenderer,)

    def __is_valid_email(self, email: str) -> bool:
        try:
            validate_email(email)
            return True
        except ValidationError:
            return False

    def post(self, request):
        email = request.data['email']
        password = request.data['password']
        user = UserModel.objects.create_user(email=email, password=password)
        if not self.__is_valid_email(email=email):
            return Response({'errors': 'The provided email is not valid'}, status=status.HTTP_400_BAD_REQUEST)
        user.save()
        return Response({'message': 'User successfully create'}, status=status.HTTP_200_OK)


class LogoutView(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message': 'success'
        }
        return response
