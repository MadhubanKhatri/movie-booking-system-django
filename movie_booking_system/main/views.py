from django.shortcuts import render,redirect
from django.contrib import messages
from .models import RegisterUser, Movie,Booking,Show

# Create your views here.

def home(request):
    return render(request, 'home.html')

def all_movies(request):
    try:
        search_query = request.GET['movie']
        if search_query:
            search_results = Movie.objects.filter(name__contains=search_query)
        else:
            search_results = Movie.objects.all()
    except:
        search_results = Movie.objects.all()
    return render(request, 'all_movies.html', {'search_results': search_results})


def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        IsUserExists = RegisterUser.objects.filter(email=email, password=password)
        if(IsUserExists):
            request.session['email'] = email
            return redirect('home')
        else:
            return render(request, 'login.html')
    else:
        return render(request, 'login.html')


def logout(request):
    del request.session['email']
    return redirect('login')

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        contact_num = request.POST['contact']
        password = request.POST['password']
        
        message = ""
        error = False

        if(username == ''):
            message = "Please enter the username."
            error = True
        elif(contact_num == ''):
            message = "Please enter the contact number."
            error = True
        elif(email == ''):
            message = "Please enter the email."
            error = True
        elif(password == ''):
            message = "Please enter the password."
            error = True
        
        if error:
            messages.warning(request, message)
            return render(request, 'register.html')
        else:
            IsUserContactExists = RegisterUser.objects.filter(contact=contact_num)
            IsUserEmailExists = RegisterUser.objects.filter(email=email)
            if(IsUserContactExists or IsUserEmailExists):
                messages.warning(request, 'User exists already. Contact number or Email must be unique.')
                return render(request, 'register.html')
            else:
                new_registration = RegisterUser.objects.create(name=username, email = email, contact=contact_num, password=password)
                return redirect('login')
    else:
        return render(request, 'register.html')
    

def movie_detail(request, movie_id):
    if 'email' in request.session:
        movie = Movie.objects.get(id=movie_id)
        show = Show.objects.filter(movie=movie)
        return render(request, 'movie_detail.html', {'movie': movie, 'shows': show})
    else:
        return redirect('login')
    


def seat_selection(request, movie_id, movie_name):
    movie = Movie.objects.get(id=movie_id)
    params = {'movie': movie}
    return render(request, 'seat_selection.html', params)

import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime

@csrf_exempt
def book_seats(request):
    if request.method == "POST":
        data = json.loads(request.body)
        
        selected_seats = data.get("seats", [])
        user  = data.get("user")
        movieID = data.get("movieId")
        show_time = data.get("showTime")    
        show_time = show_time.replace("p.m.", "PM").replace("a.m.", "AM").replace(".", "")
        show_time = datetime.strptime(show_time, "%I %p").strftime("%H:%M:%S")
        current_date = datetime.now().strftime("%Y-%m-%d")
        amount = len(selected_seats) * 100

        user_obj = RegisterUser.objects.get(email=user)
        movie_obj = Movie.objects.get(id=movieID)
        show_obj = Show.objects.get(movie=movie_obj, time=show_time)

        IsSeatBooked = False

        existing_bookings = Booking.objects.filter(movie=movie_obj,show=show_obj,date=current_date)
            

        booked_seats = set()
        for booking in existing_bookings:
            booked_seats.update(booking.seats.split(","))

        # Check for intersection of selected seats with already booked seats
        conflict_seats = set(selected_seats) & booked_seats
        print("conflict: ",conflict_seats)
        if conflict_seats:
            
            return JsonResponse({"message": "Seats are already booked.", "status": "booked"})
        else:
            Booking.objects.create(user=user_obj,movie=movie_obj,show=show_obj,date=current_date,time=show_time,
                               seats=",".join(map(str, selected_seats)),amount=amount, status=True)
            return JsonResponse({"message": "Seats booked successfully", "seats": selected_seats})
        
       
        # print(data)
        # print(selected_seats)
        
        
    return JsonResponse({"error": "Invalid request"}, status=400)
