from django.db import models

# Create your models here.

# models.py

# models.py

from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    # Adicione campos personalizados, se necessário
    pass


