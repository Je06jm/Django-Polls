from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import ugettext_lazy


class UserManager(BaseUserManager):
    """
    Add Docstring here
    """

    def create_user(self, username, password, **extra_fields):
        if not username:
            raise ValueError(ugettext_lazy("The Username must be set"))

        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, password, **extra_fields):
        if not username:
            raise ValueError(ugettext_lazy("The Username must be set"))

        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_staff", True)

        if extra_fields.get("is_superuser") is not True:
            raise ValueError(ugettext_lazy("Superuser must have is_superuser=True."))
        if extra_fields.get("is_staff") is not True:
            raise ValueError(ugettext_lazy("Superuser must have is_staff=True."))

        return self.create_user(username, password, **extra_fields)
