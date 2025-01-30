from django.shortcuts import render, redirect
from django.http import HttpResponse
from main.models import Movie

# Create your views here.
def admin_login(request):
    if 'admin_user' in request.session:
        return redirect('dashboard')
    else:
        if request.method == 'POST':
            username = request.POST['uname']
            password = request.POST['password']
            if username == 'admin' and password == 'admin':
                request.session['admin_user'] = username
                return redirect('dashboard')
            else:
                return render(request, 'admin_login.html')
        return render(request, 'admin_login.html')


def dashboard(request):
    if 'admin_user' in request.session:
        all_movies = Movie.objects.all()
        params = {'movies': all_movies}
        return render(request, 'dashboard.html', params)
    else:
        return redirect('admin_login')
    
def add_movie(request):
    if request.method == 'POST':
        movie_name = request.POST['movie_name']
        genre = request.POST['genre']
        director = request.POST['director']
        language = request.POST['language']
        release_date = request.POST['release_date']
        description = request.POST['description']
        duration = request.POST['duration']
        cast = request.POST['cast']

        addMovie = Movie(name=movie_name, genre=genre, director=director, langauge=language, 
                         release_date=release_date, description=description, duration=duration, cast=cast)
        addMovie.save()
    return redirect('dashboard')


def delete_movie(request, movie_id):
    get_movie_obj = Movie.objects.get(id=movie_id)
    get_movie_obj.delete()
    return redirect('dashboard')
    

def edit_movie(request, movie_id):
    if request.method == 'POST':
        get_movie_obj = Movie.objects.get(id=movie_id)

        movie_name = request.POST['movie_name']
        genre = request.POST['genre']
        director = request.POST['director']
        duration = request.POST['duration']
        language = request.POST['language']
        cast = request.POST['cast']
        release_date = request.POST['release_date']
        description = request.POST['description']
        get_movie_obj.name = movie_name
        get_movie_obj.genre = genre
        get_movie_obj.director = director
        get_movie_obj.duration = duration
        get_movie_obj.langauge = language
        get_movie_obj.cast = cast
        get_movie_obj.release_date = release_date
        get_movie_obj.description = description
        get_movie_obj.save()
        
    return redirect('dashboard')


def admin_logout(request):
    if 'admin_user' in request.session:
        del request.session['admin_user']
    return redirect('admin_login')
    