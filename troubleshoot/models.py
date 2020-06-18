from django.db import models

# Create your models here.
class issue(models.Model):
    issueID             = models.IntegerField(auto_created=True, primary_key=True)
    issueType           = models.CharField(max_length=30, default='')
    issueDescription    = models.CharField(max_length=250, default='')
    issueCreatedDate    = models.DateField()
    issueCreatedBy      = models.ForeignKey(User, on_delete=models.CASCADE)
    issueResolved       = models.BooleanField(default=False)
    issueNote           = models.CharField(max_length=250, default='')
    issueEditable       = models.BooleanField(default=False)

