from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User, auth
from django.contrib import messages
from . models import *
from django.contrib.auth.decorators import login_required
from emailsend import OTGGenerator

from django.urls import reverse
from .forms import PaymentInitForm

import json
import requests
from django.conf import settings
from django.shortcuts import get_object_or_404


api_key = settings.PAYSTACK_TEST_SECRETE_KEY
url = settings.PAYSTACK_INITIALIZE_PAYMENT_URL

# Create your views here.


def Home(request):
    try:
        trip_round = Trip_Round.objects.all().order_by('title')
        flight = Flight_Class.objects.all().order_by('name')
        location = Location.objects.all().order_by('name')

        return render(request, "index.html", {"rounds": trip_round, "flights": flight, "locations": location})
    
    except Exception as ex:
        print(ex)



def FlightLetter(request):
    try:
        if request.method=="POST":
            email = request.POST['newsletter_email']

            flight_letter = Flight_Letter(
                email=email
                )
            flight_letter.save()

            OTGGenerator([email], "SUBSCRIBTION TO EXCLUSIVE OFFER NEWS!!!", """We kindly inform you that you have subscribe to our news letter for frequent exclusive offer updates""")
            messages.success(request, 'You have successfully subscribe to our exclusive offer updates')
            return render(request, "index.html")

    except Exception as ex:
        print(ex)



def BookingFilter(request):
    try:
        trip_round = request.POST["trip_round"]
        flight = request.POST["flight"]
        depart_from = request.POST["depart_from"]
        destination = request.POST["destination"]

        booking_info = {
            "round_id": trip_round, 
            "flight_class_id": flight, 
            "depart_from_id": depart_from, 
            "destination_id": destination
        }

        booking = Booking.objects.filter(
            round_id=int(trip_round), 
            flight_class_id=int(flight), 
            depart_from_id=int(depart_from), 
            destination_id=int(destination)
            )
        
        request.session["booking_info"] = booking_info

        return render(request, "booking.html", {"bookings": booking})
    
    except Exception as ex:
        print(ex)     



def SortBookingFilter(request, sort_booking):
    try:
        booking_info = request.session["booking_info"]

        trip_round = booking_info["round_id"]
        flight = booking_info["flight_class_id"]
        depart_from = booking_info["depart_from_id"]
        destination = booking_info["destination_id"]

        if sort_booking == "cheapest":
            results = Booking.objects.filter(
                round_id=int(trip_round), 
                flight_class_id=int(flight), 
                depart_from_id=int(depart_from), 
                destination_id=int(destination)
            ).order_by('price')
            return render(request, "booking.html", {"bookings": results})

        elif sort_booking == "fastest":
            results = Booking.objects.filter(
                round_id=int(trip_round), 
                flight_class_id=int(flight), 
                depart_from_id=int(depart_from), 
                destination_id=int(destination)
            ).order_by('stops')
            return render(request, "booking.html", {"bookings": results})
        
        elif sort_booking == "earliest":
            results = Booking.objects.filter(
                round_id=int(trip_round), 
                flight_class_id=int(flight), 
                depart_from_id=int(depart_from), 
                destination_id=int(destination)
            ).order_by('departure')
            return render(request, "booking.html", {"bookings": results})
        
        elif sort_booking == "airline":
            results = Booking.objects.filter(
                round_id=int(trip_round), 
                flight_class_id=int(flight), 
                depart_from_id=int(depart_from), 
                destination_id=int(destination)
            ).order_by('airline')
            return render(request, "booking.html", {"bookings": results})
        
    except Exception as ex:
        print(ex)    



def Book(request, id):
    try:
        booking = Booking.objects.get(pk = id)
        
        request.session["book"] = {
            "id": str(booking.id),
            "airlineName": booking.airline.name,
            "offerName": booking.offer.name,
            "roundTitle": booking.round.title,
            "flight_className": booking.flight_class.name,
            "depart_fromName": booking.depart_from.name,
            "destinationName": booking.destination.name,
            "departure": str(booking.departure),
            "arrival": str(booking.arrival),
            # "departure_2": 
            "stops": str(booking.stops),
            "each_extra_luggage_price": str(booking.each_extra_luggage_price),
            "price": str( booking.price)
        }
        book = request.session["book"]

        return render(request, "checkout.html", {"book": book})
    
    except Exception as ex:
        print(ex)



# @login_required
def BookingCheckout(request): 
    try:
        if request.method=="POST":
            booking_id = request.POST['booking_id']
            first_name = request.POST['first_name'] 
            last_name = request.POST['last_name']
            middle_name = request.POST['middle_name']
            nationality = request.POST['nationality']
            date_of_birth = request.POST['date_of_birth']
            gender = request.POST['gender']

            passport_no = request.POST['passport_no']
            passport_expiry_date = request.POST['passport_expiry_date']
            passport_issuing_authority = request.POST['passport_issuing_authority']

            contact = request.POST['contact']
            mail = request.POST.get('email', False)
            address = request.POST['address']

            # seat_no = request.POST['seat_no']
            extra_luggage_quantity = request.POST['extra_luggage_quantity']
            extra_luggage_price = request.POST['extra_luggage_price']
            total_fare = request.POST['total_fare']

            checkout_info = {
                "booking_id": booking_id,
                "first_name": first_name,
                "last_name": last_name,
                "middle_name": middle_name,
                "nationality": nationality,
                "date_of_birth": date_of_birth,
                "gender": gender,
                "passport_no": passport_no,
                "passport_expiry_date": passport_expiry_date,
                "passport_issuing_authority": passport_issuing_authority,
                "contact": contact,
                "mail": mail,
                "address": address,
                # "seat_no": seat_no,
                "extra_luggage_quantity": extra_luggage_quantity,
                "extra_luggage_price": extra_luggage_price,
                "total_fare": total_fare
            }

            request.session["checkout_info"] = checkout_info

            checkout_info = request.session["checkout_info"]
            book = request.session["book"]

            if len(contact) != 11:
                messages.error(request, 'Contact format not accepted')
                return render(request, "checkout.html", {"checking": checkout_info, "book": book})    
            
            elif gender == 'male' or gender == 'female':    

                if request.user.is_authenticated:
                    user_id = request.session["userId"]  
                    user = User.objects.get(pk = user_id)
                    booking = Booking.objects.get(pk = booking_id)

                    checkout = Checkout(
                        user = user,
                        booking = booking,
                        first_name=first_name, 
                        last_name=last_name,
                        middle_name=middle_name,
                        nationality=nationality,
                        date_of_birth=date_of_birth,
                        gender=gender,
                        passport_no=passport_no,
                        passport_expiry_date=passport_expiry_date,
                        passport_issuing_authority=passport_issuing_authority,
                        contact=contact,
                        mail=mail,
                        address=address,
                        # seat_no=seat_no,
                        extra_luggage_quantity=extra_luggage_quantity,
                        extra_luggage_price=extra_luggage_price,
                        total_fare=total_fare
                        )
                    checkout.save()

                    return redirect('create')
                return redirect("login")
            
            messages.error(request, 'Gender not accepted')
            return render(request, "checkout.html", {"checking": checkout_info, "book": book})
                    
        elif request.method=="GET":
            return redirect("home")
            
    except Exception as ex:
        print(ex) 



# account

def Register(request):
    try:
        if request.method=='POST':
            username = request.POST['username']
            email = request.POST['email']
            password = request.POST['password']
            confirm_password = request.POST['confirm_password']

            if password==confirm_password:                                
                if User.objects.filter(username=username).exists():
                    messages.error(request, 'Username taken')
                    return redirect("register")  
                
                else:
                    user = User.objects.create_user(
                        username=username,
                        email=email,  
                        password=password
                        )
                    user.save()

                    OTGGenerator([email], "SUCCESSFUL REGISTRATION!!!", """We kindly inform you that you have sucessfully register your account on Airline-Booking""")
                    return render(request, "login.html", {"user": user}) 

            else:
                messages.error(request, 'Password not the same')
                return redirect("register") 
            
        elif request.method=='GET': 
            return render(request, "register.html") 

    except Exception as ex:
        print(ex)    



def Login(request):
    try:
        if request.method=='POST':
            username = request.POST['username']
            password = request.POST['password']
            
            user = auth.authenticate(username=username, password=password)

            if user is not None:
                auth.login(request, user)

                request.session["userId"] = user.id
                request.session["username"] = user.username
                request.session["email"] = user.email
                email = request.session["email"]

                session_keys = list(request.session.keys())
                if "checkout_info" in session_keys:
                    checkout_info = request.session["checkout_info"]
                    
                    if checkout_info is not None:
                        book = request.session["book"]
                        
                        OTGGenerator([email], "SUCCESSFUL LOGIN!!!", """We kindly inform you that you have sucessfully login your account on Airline-Booking""")
                        messages.success(request, 'You have successfully login')
                        return render(request, "checkout.html", {"checking": checkout_info, "book": book})
                    
                    else:
                        OTGGenerator([email], "SUCCESSFUL LOGIN!!!", """We kindly inform you that you have sucessfully login your account on Airline-Booking""")
                        return redirect("home")

                OTGGenerator([email], "SUCCESSFUL LOGIN!!!", """We kindly inform you that you have sucessfully login your account on Airline-Booking""")   
                return redirect("home")
            
            else:
                messages.error(request, 'Incorrect username or password')
                return render(request, "login.html") 
            
        elif request.method=='GET':
            return render(request, "login.html") 
                
    except Exception as ex:
        print(ex)



def payment_init(request):
    if request.method == 'POST':
        # get form data if POST request
        form = PaymentInitForm(request.POST)

        # validate form before saving
        if form.is_valid():
            payment = form.save(commit=False)
            payment.save()
            # set the payment in the current session
            request.session['payment_id'] = payment.id
            # message alert to confirm payment intializaton
            # messages.success(request, "Payment Initialized Successfully." )  <-----
            # redirect user for payment completion
            return redirect(reverse('process'))
    else:
    # render form if GET request
        form = PaymentInitForm()
    return render(request, 'create.html', {'form': form})



def payment_process(request):
    # retrive the payment_id we'd set in the djago session ealier
    payment_id = request.session.get('payment_id', None)
    # using the payment_id, get the database object
    payment = get_object_or_404(Payment, id=payment_id)
    # retrive payment amount 
    amount = payment.get_amount()

    if request.method == 'POST':
        success_url = request.build_absolute_uri(
            reverse('success'))
        cancel_url = request.build_absolute_uri(
            reverse('canceled'))

        # metadata to pass additional data that 
        # the endpoint doesn't accept naturally.
        metadata= json.dumps({"payment_id":payment_id,  
                              "cancel_action":cancel_url,   
                            })

        # Paystack checkout session data
        session_data = {
            'email': payment.email,
            'amount': int(amount),
            'callback_url': success_url,
            'metadata': metadata
            }

        headers = {"authorization": f"Bearer {api_key}"}
        # API request to paystack server
        r = requests.post(url, headers=headers, data=session_data)
        response = r.json()
        if response["status"] == True :
            # redirect to Paystack payment form
            try:
                redirect_url = response["data"]["authorization_url"]
                return redirect(redirect_url, code=303)
            except:
                pass
        else:
            return render(request, 'process.html', locals())
    else:
        return render(request, 'process.html', locals())
    


def payment_success(request):

    payment_id = request.session.get('payment_id', None)#new
    # using the payment_id, get the database object
    payment = get_object_or_404(Payment, id=payment_id)#new

    # retrive the query parameter from the request object
    ref = request.GET.get('reference', '')#new
    # verify transaction endpoint
    url = 'https://api.paystack.co/transaction/verify/{}'.format(ref)#new

    # set auth headers
    headers = {"authorization": f"Bearer {api_key}"}#new
    r = requests.get(url, headers=headers)#new
    res = r.json()#new
    res = res["data"]

    # verify status before setting payment_ref
    if res['status'] == "success":  # new
        # update payment payment reference
        payment.paystack_ref = ref #new
        payment.save()#new

        # del request.session["booking_info"]
        # del request.session["checkout_info"]
        # del request.session["book"]      

    return render(request, 'success.html')


def payment_canceled(request):
    return render(request, 'canceled.html')
    


def Logout(request):
    session_keys = list(request.session.keys())
    for key in session_keys:
        del request.session[key]
    auth.logout(request)
    return redirect("home") 



