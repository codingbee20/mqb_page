from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import Group
# Create your models here.


class Holiday(models.Model):
    date = models.DateField()


class ActivitiesTask(models.Model):
    group_name = models.ForeignKey(Group, on_delete=models.CASCADE)
    task_name = models.CharField(max_length=100)


class MonthlyProductivity(models.Model):
    activity_task = models.ForeignKey(ActivitiesTask, on_delete=models.CASCADE)
    year = models.IntegerField(default=2000, validators=[MaxValueValidator(2050), MinValueValidator(2000)])
    month = models.IntegerField(default=1, validators=[MaxValueValidator(12), MinValueValidator(1)])
    pys = models.FloatField(default=0)
