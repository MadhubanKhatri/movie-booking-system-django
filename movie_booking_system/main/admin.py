from django.contrib import admin
from .models import RegisterUser, Booking, Movie

# Register your models here.
class RegisterUserAdmin(admin.ModelAdmin):
    # Display fields in the list view
    list_display = ('name', 'email', 'contact')

    # Add search functionality
    search_fields = ('name', 'email')

    # Add filters
    list_filter = ('contact',)

class BookingAdmin(admin.ModelAdmin):
    # Display fields in the list view
    list_display = ('user', 'movie', 'date', 'time', 'seats', 'amount', 'status')

    # Add search functionality
    search_fields = ('user', 'movie')

    # Add filters
    list_filter = ('status',)


class MovieAdmin(admin.ModelAdmin):
    # Display fields in the list view
    list_display = ('name', 'description')

    # Add search functionality
    search_fields = ('name', 'description')

    # Add filters
    list_filter = ('name',)

# Register the model with the custom admin class
admin.site.register(RegisterUser, RegisterUserAdmin)
admin.site.register(Booking, BookingAdmin)
admin.site.register(Movie, MovieAdmin)