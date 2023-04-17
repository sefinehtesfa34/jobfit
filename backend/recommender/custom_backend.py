from typing import Any, Optional
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.base_user import AbstractBaseUser
from django.http import HttpRequest
from django.contrib.auth import get_user_model
UserModel = get_user_model()
class CustomBackend(ModelBackend):
    def authenticate(self, email, password) -> Optional[AbstractBaseUser]:
        try:
            user = UserModel.objects.get(email = email)
        except UserModel.DoesNotExist:
            return None 
        if user.check_password(password):
            return user 
        return None 
    