from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('all_movies/', views.all_movies, name='all_movies'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
]
