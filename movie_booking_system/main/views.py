from django.shortcuts import render,redirect
from django.contrib import messages

# Create your views here.
def home(request):
    return render(request, 'home.html')

def all_movies(request):
    return render(request, 'all_movies.html')


def login(request):
    return render(request, 'login.html')

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
            print("redirect login")
            return redirect('login')
    else:
        print('no post')
        return render(request, 'register.html')