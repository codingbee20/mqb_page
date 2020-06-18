from django.contrib import admin
from .models import Holiday, MonthlyProductivity, ActivitiesTask
# Register your models here.

admin.site.register(Holiday)
admin.site.register(MonthlyProductivity)
admin.site.register(ActivitiesTask)
