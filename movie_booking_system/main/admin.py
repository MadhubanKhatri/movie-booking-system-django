from django.contrib import admin
from .models import RegisterUser, Booking, Movie, Theatre,Show, Payment

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
    list_display = ('user', 'movie','show', 'date', 'time', 'seats', 'amount', 'status')

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


class TheatreAdmin(admin.ModelAdmin):
    # Display fields in the list view
    list_display = ('name', 'address', 'contact')

    # Add search functionality
    search_fields = ('name', 'address')

    # Add filters
    list_filter = ('name',)


class ShowAdmin(admin.ModelAdmin):
    # Display fields in the list view
    list_display = ('movie', 'theatre', 'date', 'time', 'price')

    # Add search functionality
    search_fields = ('movie', 'theatre')

    # Add filters
    list_filter = ('price',)


class PaymentAdmin(admin.ModelAdmin):
    # Display fields in the list view
    list_display = ('user', 'order_id', 'amount', 'payment_status', 'created_at')

    # Add filters
    list_filter = ('user__name','payment_status')


# Register the model with the custom admin class
admin.site.register(RegisterUser, RegisterUserAdmin)
admin.site.register(Booking, BookingAdmin)
admin.site.register(Movie, MovieAdmin)
admin.site.register(Theatre, TheatreAdmin)
admin.site.register(Show, ShowAdmin)
admin.site.register(Payment, PaymentAdmin)