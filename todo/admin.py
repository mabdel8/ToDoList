from django.contrib import admin
from .models import Task, Topic

# Register your models here.
admin.site.register(Task)
admin.site.register(Topic)