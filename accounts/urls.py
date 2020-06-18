from django.urls import path, include
from . import views


urlpatterns = [
    path('signup/', views.SignUp.as_view(), name='signup'),
	path('accounts/login/', include('django.contrib.auth.urls'), name='login'),
    path('', views.login),
    path('profile/<int:pk>/', views.profile, name='profile')
]