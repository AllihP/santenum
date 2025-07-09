from django.db import models
from django.core.validators import RegexValidator, FileExtensionValidator
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from django.core.exceptions import ValidationError
import os


