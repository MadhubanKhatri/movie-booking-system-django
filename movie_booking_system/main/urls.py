from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('all_movies/', views.all_movies, name='all_movies'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('register/', views.register, name='register'),
    
    path('movie_detail/<int:movie_id>/', views.movie_detail, name='movie_detail'),
    path('movie_detail/select_seat/<int:movie_id>/<str:movie_name>/<str:show_price>/', views.seat_selection, name='seat_selection'),
    path("booked-seats/", views.booked_seats, name="booked_seats"),
    path("booking_history/", views.booking_history, name="booking_history"),
    path("payment_checkout/", views.payment_checkout, name="payment_checkout"),
    path('paymenthandler/', views.paymenthandler, name='paymenthandler'),
]
