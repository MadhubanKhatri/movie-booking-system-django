from django.db import models

# Create your models here.
class RegisterUser(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)  # Name cannot be null
    email = models.EmailField(unique=True, null=False, blank=False)  # Email must be unique
    contact = models.CharField(max_length=15, blank=True, null=True)  # Optional contact field
    password = models.CharField(max_length=255)  # Password field


    def __str__(self):
        return self.name



class Movie(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    #image = models.ImageField(upload_to='movie_images/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name


class Booking(models.Model):
    user = models.ForeignKey(RegisterUser, on_delete=models.CASCADE)
    movie = models.CharField(max_length=100)
    date = models.DateField()
    time = models.TimeField()
    seats = models.IntegerField()
    amount = models.FloatField()
    status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.movie