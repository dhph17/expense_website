
from django.urls import path
from . import views
app_name = 'users'
urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.registerUser.as_view(), name='registerUser'),
    path('login/', views.loginUser.as_view(), name='loginUser'),
    path('logout/', views.logoutUser, name='logoutUser'),
    path('check_username/', views.check_username, name='check_username'),
    path('check_email/', views.check_email, name='check_email'),
]
