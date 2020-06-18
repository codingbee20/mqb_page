from django.urls import path, re_path
from . import views


urlpatterns = [
    re_path(r'^productivity/$', views.productivity_management, name='productivity_management'),
    re_path(r'^tasks_tracking/$', views.tasks_management, name='tasks_management'),
    re_path(r'holiday/$', views.holiday, name='holiday'),
    re_path(r'monthly_productivity/$', views.monthly_productivity, name='monthly_productivity'),
    path('baseline/', views.baseline_effort, name='baseline'),
    re_path(r'^exportdata/$', views.export_data, name='exportdata'),

]
