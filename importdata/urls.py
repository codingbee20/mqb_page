from django.urls import path, re_path
from . import views


urlpatterns = [
    re_path(r'', views.import_data, name='IO_port'),

]