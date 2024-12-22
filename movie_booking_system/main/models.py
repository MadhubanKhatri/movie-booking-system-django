from django.db import models

# Create your models here.
class RegisterUser(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)  # Name cannot be null
    email = models.EmailField(unique=True, null=False, blank=False)  # Email must be unique
    contact = models.CharField(max_length=15, blank=True, null=True)  # Optional contact field
    password = models.CharField(max_length=255)  # Password field


    def __str__(self):
        return self.name