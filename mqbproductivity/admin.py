from django.contrib import admin
from .models import Effort, Daily, TaskCategory, TasksTracking, BlockData
# Register your models here.

admin.site.register(Daily)
admin.site.register(Effort)
admin.site.register(TaskCategory)
admin.site.register(TasksTracking)
admin.site.register(BlockData)
