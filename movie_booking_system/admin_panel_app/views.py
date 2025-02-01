from django.shortcuts import render, redirect
from main.models import Movie, Show, Theatre, RegisterUser, Booking
from django.utils import timezone
from datetime import timedelta

# Create your views here.
def admin_login(request):
    if 'admin_user' in request.session:
        return redirect('movies')
    else:
        if request.method == 'POST':
            username = request.POST['uname']
            password = request.POST['password']
            if username == 'admin' and password == 'admin':
                request.session['admin_user'] = username
                return redirect('movies')
            else:
                return render(request, 'admin_login.html')
        return render(request, 'admin_login.html')


def dashboard(request):
    if 'admin_user' not in request.session:
        return redirect('admin_login')
    else:
        from django.db.models import Sum,Count
        total_users = RegisterUser.objects.count()
        total_shows = Show.objects.count()
        total_tickets = Booking.objects.filter(status=True).count()
        total_revenue = Booking.objects.aggregate(Sum('amount'))['amount__sum']

        most_booked_show = Booking.objects.values('movie__name').annotate(total_bookings=Count('id')).order_by('-total_bookings')[:10]
        most_booked_theatres = Booking.objects.values('show__theatre__name').annotate(total_bookings=Count('id')).order_by('-total_bookings')[:10]
        
        one_week_ago = timezone.now().date() - timedelta(days=7)
        active_users = Booking.objects.filter(date__gte=one_week_ago).values('user__email').distinct()
        
        param = {'users_count': total_users, 'shows_count': total_shows, 
                 'tickets_count': total_tickets, 'revenue':total_revenue, 'most_booked_show': most_booked_show, 'most_booked_theatres': most_booked_theatres, 'active_users': active_users}
        return render(request, 'dashboard.html', param)
    

def movies(request):
    if 'admin_user' in request.session:
        all_movies = Movie.objects.all()
        params = {'movies': all_movies}
        return render(request, 'movies.html', params)
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
    return redirect('movies')


def delete_movie(request, movie_id):
    get_movie_obj = Movie.objects.get(id=movie_id)
    get_movie_obj.delete()
    return redirect('movies')
    

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
        
    return redirect('movies')


def admin_logout(request):
    if 'admin_user' in request.session:
        del request.session['admin_user']
    return redirect('admin_login')


def shows(request):
    all_shows = Show.objects.all().order_by('-id')
    all_movies = Movie.objects.all()
    all_theatre = Theatre.objects.all()
    params = {"shows": all_shows, "movies": all_movies, "theatres": all_theatre}
    return render(request, "shows.html", params)
    
def add_show(request):
    if request.method == 'POST':
        movieId = request.POST['movie_id']
        theatreId = request.POST['movie_id']
        date = request.POST['date']
        time = request.POST['time']

        price = request.POST['price']
        movieObj = Movie.objects.get(id=movieId)
        theatreObj = Theatre.objects.get(id=theatreId)

        addShow = Show(movie=movieObj, theatre=theatreObj, date=date, time=time, price=price)
        addShow.save()
        
    return redirect('shows')

def delete_show(request, show_id):
    get_show_obj = Show.objects.get(id=show_id)
    get_show_obj.delete()
    return redirect('shows')


def edit_show(request, show_id):
    if request.method == 'POST':
        get_show_obj = Show.objects.get(id=show_id)

        movieId = request.POST['movie_id']
        theatreId = request.POST['theatre_id']
        date = request.POST['date']
        time = request.POST['time']
        price = request.POST['price']
        
        movieObj = Movie.objects.get(id=movieId)
        theatreObj = Theatre.objects.get(id=theatreId)
        
        get_show_obj.movie = movieObj
        get_show_obj.theatre = theatreObj
        get_show_obj.date = date
        get_show_obj.time = time
        get_show_obj.price = price
        
        get_show_obj.save()
        
    return redirect('shows')


