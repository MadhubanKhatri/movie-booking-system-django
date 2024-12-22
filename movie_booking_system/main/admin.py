from django.contrib import admin
from .models import RegisterUser

# Register your models here.
class RegisterUserAdmin(admin.ModelAdmin):
    # Display fields in the list view
    list_display = ('name', 'email', 'contact')

    # Add search functionality
    search_fields = ('name', 'email')

    # Add filters
    list_filter = ('contact',)

# Register the model with the custom admin class
admin.site.register(RegisterUser, RegisterUserAdmin)