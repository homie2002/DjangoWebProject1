"""
Definition of models.
"""

from django.db import models

# Create your models here.
class SpeedTestResult(models.Model):
    download_speed = models.FloatField()
    upload_speed = models.FloatField()
    unique_link = models.CharField(max_length=100, unique=True)