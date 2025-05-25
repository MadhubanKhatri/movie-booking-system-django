from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib import messages
from .models import RegisterUser, Movie,Booking,Show,Payment, Theatre
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
import razorpay
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest
from django.urls import reverse
from django.http import HttpRequest

# authorize razorpay client with API Keys.
razorpay_client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))


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
                RegisterUser.objects.create(name=username, email = email, contact=contact_num, password=password)
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
    


def seat_selection(request, movie_id, movie_name,show_price):
    
    movie = Movie.objects.get(id=movie_id)
    params = {'movie': movie}
    return render(request, 'seat_selection.html', params)

def payment_checkout(request):
    if request.method == "POST":
        data = json.loads(request.body)
        request.session['data'] = data

        total_seats_count = len(data.get("seats", []))
        show_price = data.get("show_price", 0)
        
        currency = 'INR'
        amount = int(float(show_price)) * total_seats_count * 100
        request.session['latest_payment_amount'] = amount
        

        # Create a Razorpay Order
        razorpay_order = razorpay_client.order.create(dict(amount=amount,
                                                        currency=currency,
                                                        payment_capture='0'))
        # order id of newly created order.
        razorpay_order_id = razorpay_order['id']
        callback_url = request.build_absolute_uri(reverse('paymenthandler'))
        
        # we need to pass these details to frontend.
        context = {}
        context['razorpay_order_id'] = razorpay_order_id
        context['razorpay_merchant_key'] = settings.RAZOR_KEY_ID
        context['razorpay_amount'] = amount
        context['currency'] = currency
        context['callback_url'] = callback_url
        return JsonResponse({"message": "checkout initiated", "context": context}, status=200)
    return JsonResponse({"message": "checkout initiated"}, status=200)


@csrf_exempt
def paymenthandler(request):

    # only accept POST request.
    if request.method == "POST":
        try:
            # get the required parameters from post request.
            payment_id = request.POST.get('razorpay_payment_id', '')
            razorpay_order_id = request.POST.get('razorpay_order_id', '')
            signature = request.POST.get('razorpay_signature', '')
            
            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            }

            # verify the payment signature.
            result = razorpay_client.utility.verify_payment_signature(params_dict)
            print(result)
            if result is not None:
                amount = request.session['latest_payment_amount']
                try:
                    data = request.session['data']
                    selected_seats = data.get("seats", [])
                    user  = data.get("user")
                    movieID = data.get("movieId")
                    theatre_id = data.get("theatre_id")
                    booking_date = data.get("booking_date")
                    show_time = data.get("showTime")    
                    show_time = show_time.replace("p.m.", "PM").replace("a.m.", "AM").replace(".", "")
                    show_time = datetime.strptime(show_time, "%I %p").strftime("%H:%M:%S")
                    
                    date_obj = datetime.strptime(booking_date, "%d-%m-%Y")
                    user_obj = RegisterUser.objects.get(email=user)
                    movie_obj = Movie.objects.get(id=movieID)
                    show_obj = Show.objects.get(movie=movie_obj,theatre=theatre_id, time=show_time)

                    existing_bookings = Booking.objects.filter(movie=movie_obj,show=show_obj,date=date_obj,time=show_time,
                                                   show__theatre__id=theatre_id)

                    booked_seats = set()
                    for booking in existing_bookings:
                        booked_seats.update(booking.seats.split(","))
                    
                    # Check for intersection of selected seats with already booked seats
                    conflict_seats = set(selected_seats) & booked_seats
                    
                    if conflict_seats:
                        return JsonResponse({"message": "Seats are already booked.", "status": "booked"})
                    else:
                        # capture the payemt
                        razorpay_client.payment.capture(payment_id, amount)
                        amount_in_rupees = amount / 100  # Convert to rupees
                        Booking.objects.create(user=user_obj,movie=movie_obj,show=show_obj,date=date_obj,time=show_time,
                                            seats=",".join(map(str, selected_seats)),amount=amount_in_rupees, status=True)
                        Payment.objects.create(user=user_obj, order_id=razorpay_order_id,amount=amount_in_rupees,
                                               payment_status="Success")
                    #return render(request, 'paymentsuccess.html', params_dict)
                    return render(request, 'payment_success.html', {'params_dict': params_dict, 'amount': amount_in_rupees})
                except:
                    print("Error in capturing payment")
                    #return render(request, 'paymentfail.html')
                    return HttpResponse("Payment failed")
            else:
                #return render(request, 'paymentfail.html')
                return HttpResponse("Payment failed")
        except:
            return HttpResponseBadRequest()
    else:
        return HttpResponseBadRequest()

@csrf_exempt
def booked_seats(request):
    if request.method == "POST":
        data = json.loads(request.body)
    
        movieID = data.get("movieId")
        user = data.get("user")
        theatreID = data.get("theatre_id")
        booking_date = data.get("booking_date")
        show_time = data.get("showTime")  
        show_time = show_time.replace("p.m.", "PM").replace("a.m.", "AM").replace(".", "")
        show_time = datetime.strptime(show_time, "%I %p").time()
        
        date_obj = datetime.strptime(booking_date, "%d-%m-%Y")
        formatted_date = date_obj.strftime("%Y-%m-%d")
        movie_obj = Movie.objects.get(id=movieID)
        show_obj = Show.objects.get(movie=movie_obj, time=show_time)
        theatre_obj = Theatre.objects.get(id=theatreID) 
        user_obj = RegisterUser.objects.get(email=user)

        existing_bookings = Booking.objects.filter(user=user_obj,movie=movie_obj,show=show_obj,date=formatted_date,time=show_time,show__theatre=theatre_obj)
        print(user_obj,movie_obj, show_obj, formatted_date, show_time, theatre_obj)
        booked_seats = set()
        for booking in existing_bookings:
            booked_seats.update(booking.seats.split(","))
        
        return JsonResponse({"status": "Booked", "seats": "Seats are already booked.", "booked_seats": list(booked_seats)})
    else:
        pass
    
    return JsonResponse({"error": "Invalid request"}, status=400)



def booking_history(request):
    if 'email' in request.session:
        user = RegisterUser.objects.get(email=request.session['email'])
        bookings = Booking.objects.filter(user=user).order_by('-created_at')
        return render(request, 'bookings.html', {'bookings': bookings})
    else:
        return redirect('login')
    

