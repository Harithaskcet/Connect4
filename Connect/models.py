from django.db import models
from django.contrib.postgres.fields import ArrayField
# Create your models here.
class Connect(models.Model):
    user = models.CharField(max_length = 255)
    moves = ArrayField(models.IntegerField())
    grid = ArrayField(ArrayField(models.IntegerField()))
