from time import time
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Topic(models.Model):
  name = models.CharField(max_length=65)

  def __str__ (self):
    return self.name


class Task(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
  name = models.CharField(max_length=100)
  topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)
  description = models.TextField(max_length=250)
  time_created = models.DateTimeField('time created', auto_now_add=True)
  completed = models.BooleanField(default=False)
  due_date = models.DateTimeField(blank=True, null=True)

  def __str__ (self):
    return self.name

  class Meta:
    ordering = ['-time_created']