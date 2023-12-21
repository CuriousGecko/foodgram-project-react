from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import UniqueConstraint

from foodgram_backend.constants import MAX_LENGHT_EMAIL, MAX_LENGHT_ROLE

# User = get_user_model()
