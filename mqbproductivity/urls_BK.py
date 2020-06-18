from django.urls import path
from . import views


urlpatterns = [
    path('<int:pk>/', views.productivity_index, name='productivity_index'),
    path('<tasks_tracking>/<int:pk>/', views.tasks_tracking, name='tasks_tracking'),
    path('about/', views.about, name='about'),
]
