from django.db import models
from django.contrib.auth.models import User
# Create your models here.

# Database for Task tracking


class TaskCategory(models.Model):
    name = models.CharField(max_length=30, primary_key=True)


class Daily(models.Model):
    date = models.DateField(primary_key=True)


class BlockData(models.Model):
    month = models.DateField()
    member = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)


class TasksTracking(models.Model):
    member = models.ForeignKey(User, on_delete=models.CASCADE)
    categories = models.ForeignKey(TaskCategory, on_delete=models.CASCADE)
    taskName = models.CharField(max_length=250, default='')
    effort_est = models.FloatField(default=0)
    startdate = models.DateField()
    stopdate = models.DateField()
    status = models.BooleanField(default=False)
    modify_status = models.BooleanField(default=False)


# Database for task daily

class Effort(models.Model):
    member = models.ForeignKey(User, on_delete=models.CASCADE)
    dateCreateTask = models.ForeignKey(Daily, on_delete=models.CASCADE)
    tasktracking = models.ForeignKey(TasksTracking, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    effort = models.FloatField(default=0)
    comment = models.TextField(default='')






