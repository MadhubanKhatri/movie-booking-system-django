from django.shortcuts import render,redirect
from django.contrib import messages
from .models import RegisterUser, Booking, Movie

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
    movie = Movie.objects.get(id=movie_id)
    return render(request, 'movie_detail.html', {'movie': movie})
