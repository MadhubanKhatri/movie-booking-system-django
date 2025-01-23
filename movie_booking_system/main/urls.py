from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('all_movies/', views.all_movies, name='all_movies'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('register/', views.register, name='register'),
    path('movie_detail/<int:movie_id>/', views.movie_detail, name='movie_detail'),
]
