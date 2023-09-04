"""
Definition of models.
"""
from django.db import models
from django.contrib.auth import get_user_model
import uuid
from datetime import datetime

User = get_user_model()
# Create your models here.
class SpeedTestResult(models.Model):
    download_speed = models.FloatField()
    upload_speed = models.FloatField()
    unique_link = models.CharField(max_length=100, unique=True)

class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    id_user = models.IntegerField()
    bio = models.TextField(blank=True)
    profileimg_path = models.CharField(max_length=255, blank=True)  # Используем CharField для хранения пути к изображению
    location = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.user.username