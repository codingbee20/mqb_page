from django.urls import path, re_path
from . import views


urlpatterns = [
    re_path(r'^$', views.productivity_index, name='productivity_index'),
    re_path(r'^tasks_tracking/$', views.tasks_tracking, name='tasks_tracking'),
    path('about/', views.about, name='about'),
]
