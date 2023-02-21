from django.contrib import admin

from .models import UserModel, TodoListModel

admin.site.register(UserModel)
admin.site.register(TodoListModel)
