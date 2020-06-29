from django.shortcuts import render
from django.contrib.auth.models import User
from . import models
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from urllib.parse import urlencode
import datetime
from datetime import datetime as datet
from django.shortcuts import render

# Create your views here.

def add_issue(user_id, ID, Type, Description, Note):
    update_issue = models.issue(
        issueID         = ID,
        issueType       = Type,
        issueDescription= Description,
        issueCreatedDate= datet.today(),
        issueCreatedBy  = user_id,
        issueNote       = Note
    )
    update_issue.save()
    return update_issue

def delete_issue(ID):
    pass


def troubleshoot_index(request):
    user_id = User.objects.get(username=request.user)
    return render(request,'troubleshoot_index.html', context)

