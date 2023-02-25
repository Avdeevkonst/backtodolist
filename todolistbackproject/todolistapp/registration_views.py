from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from .renderers import UserJSONRenderer
from .models import UserModel
from .serializers import UserSerializer, RegistrationSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import GenericAPIView
from django.http import JsonResponse


# class UserAuthenticationView(GenericAPIView):
#     serializer_class = LoginSerializer
#
#     def post(self, request):
#         serializer = self.serializer_class(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         return JsonResponse(serializer.data, status=status.HTTP_200_OK)


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
        return Response({'message': 'User successfully create'}, status=status.HTTP_201_CREATED)


class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
