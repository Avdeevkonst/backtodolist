from .registration_views import UserAuthenticationView,\
    LogoutView, UserRegistrationView
from django.urls import path, include
from .views import TodolistDetail, TodolistCreate, UserView

urlpatterns = [
    # path('auth/login', UserAuthenticationView.as_view(), name='login'),
    path('register', UserRegistrationView.as_view(), name='register'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('', UserView.as_view(), name='user'),
    path('tododetail', TodolistDetail.as_view(), name='todolist'),
    path('todolistcreate', TodolistCreate.as_view(), name='create'),
]
