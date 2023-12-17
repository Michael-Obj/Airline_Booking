from django.db import models
from django.contrib.auth.models import User
import uuid

# Create your models here.  


class Airline(models.Model):
    name = models.CharField(max_length=200)
    model = models.CharField(max_length=200, null=True)
    seat_numbers = models.PositiveIntegerField(default=0, null=True)

    def __str__(self):
        return f"{self.name}: {self.seat_numbers}"


class Trip_Round(models.Model):
    title = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return f"{self.title}"


class Flight_Class(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)
    
    def __str__(self):
        return f"{self.name}"


class Offer(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True, default="default")

    def __str__(self):
        return f"{self.name}"
        
        
class Location(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)
    address = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.name}"


class Booking(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    round = models.ForeignKey(Trip_Round, on_delete=models.CASCADE)
    flight_class = models.ForeignKey(Flight_Class, on_delete=models.CASCADE, default=None)
    offer = models.ForeignKey(Offer, on_delete=models.CASCADE, default=None)
    airline = models.ForeignKey(Airline, on_delete=models.CASCADE, default=None)

    depart_from = models.ForeignKey(Location, on_delete=models.CASCADE, default=None, related_name="booking_depart_from")
    destination = models.ForeignKey(Location, on_delete=models.CASCADE, default=None, related_name="booking_destination")
    departure = models.DateTimeField(default=None)
    arrival = models.DateTimeField(default=None)
    departure_2 = models.DateTimeField(default=None, null=True, blank=True)
    arrival_2 = models.DateTimeField(default=None, null=True, blank=True)
    passenger = models.CharField(default=1)
  
    stops = models.PositiveIntegerField(default=0)
    price = models.DecimalField(decimal_places=2, max_digits=20, default=0)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.airline.name} > {self.depart_from} - {self.destination}: {self.departure}"
        



class Checkout(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, default=None)
    
    # primary info
    first_name = models.CharField(max_length=250, default=None)
    last_name = models.CharField(max_length=250, default=None)
    middle_name = models.CharField(max_length=250, default=None)
    nationality = models.CharField(default=None)
    date_of_birth = models.DateField(default=None)
    gender= models.CharField(max_length=25, default=None)

    # traveling credentials
    passport_no = models.CharField(default=None)
    passport_expiry_date = models.DateField(default=None)
    passport_issuing_authority = models.CharField(default=None)

    # where to send confirmation
    contact = models.CharField(max_length=15)
    mail = models.EmailField()
    address = models.TextField()

    # others 
    seat_no = models.PositiveIntegerField(unique=False)
    extra_luggage = models.CharField(default=0)

    total_fare = models.DecimalField(decimal_places=2, max_digits=20)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name}-{self.last_name}: {self.seat_no}"




class Flight_Status(models.Model):
    status = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return f"{self.status}"
    

class Ticket(models.Model):
    checkout = models.ForeignKey(Checkout, on_delete=models.CASCADE)
    flight_status = models.ForeignKey(Flight_Status, on_delete=models.CASCADE, default=None)
    
    def __str__(self):
        return f"{self.checkout.first_name}: {self.flight_status}"
    



class Payment(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    city = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paystack_ref = models.CharField(max_length=15, blank=True)
    paid = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return f'Payment {self.id}'

    def get_amount(self):
        return self.amount
