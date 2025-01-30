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
    langauge = models.CharField(max_length=50,default='None')
    genre = models.CharField(max_length=200,default='None')
    duration = models.CharField(max_length=50,default='None')
    cast = models.TextField(default='None')
    director = models.CharField(max_length=100, default='None')
    release_date = models.DateField(null=True, blank=True,default='2025-01-01') 
    #image = models.ImageField(upload_to='movie_images/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name


class Theatre(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField()
    contact = models.CharField(max_length=15)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    


class Show(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    theatre = models.ForeignKey(Theatre, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    price = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.movie.name
    


class Booking(models.Model):
    user = models.ForeignKey(RegisterUser, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    show = models.ForeignKey(Show, on_delete=models.CASCADE, default='1')
    date = models.DateField()
    time = models.TimeField()
    seats = models.CharField(max_length=100)
    amount = models.FloatField()
    status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.movie.name



