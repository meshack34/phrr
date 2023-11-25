# myapp/authentication.py

from django.contrib.auth.backends import ModelBackend
from .models import Account

class MyCustomBackend(ModelBackend):
    def authenticate(self, request, account_id=None, password=None, **kwargs):
        try:
            user = Account.objects.get(account_id=account_id)
        except Account.DoesNotExist:
            return None

        if user.check_password(password):
            return user
        return None

    def get_user(self, user_id):
        try:
            return Account.objects.get(pk=user_id)
        except Account.DoesNotExist:
            return None
