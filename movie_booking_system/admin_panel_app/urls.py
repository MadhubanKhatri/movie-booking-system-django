from django.urls import path
from . import views


urlpatterns = [
    path('login/', views.admin_login, name='admin_login'),
    path('logout/', views.admin_logout, name='admin_logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('movies/', views.movies, name='movies'),
    path('add_movie/', views.add_movie, name='add_movie'),
    path('edit_movie/<int:movie_id>/', views.edit_movie, name='edit_movie'),
    path('delete_movie/<int:movie_id>/', views.delete_movie, name='delete_movie'), 

    path('shows/', views.shows, name='shows'),
    path('add_show/', views.add_show, name='add_show'),
    path('edit_show/<int:show_id>/', views.edit_show, name='edit_show'),
    path('delete_show/<int:show_id>/', views.delete_show, name='delete_show'), 
]
