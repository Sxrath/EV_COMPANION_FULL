from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy,reverse
from django.contrib.auth.models import User
from . import models
from django import forms
from django.contrib.auth import authenticate,logout,login
from django.contrib.auth.views import LoginView,LogoutView
from django.views.generic import ListView,CreateView,UpdateView,DeleteView,DetailView

def register(request):
    if request.method == "POST":
        user = User.objects.create(username = request.POST.get('username'),email = request.POST.get('email'))
        user.set_password(request.POST.get('password'))
        user.save()

        return HttpResponseRedirect(reverse('home'))
    else:
        return render(request,'register.html')


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username = username,password = password)
        if user:
            if user.is_active:
                login(request, user)
                
                return HttpResponseRedirect(reverse('home'))
        else:
            print("No such user")

            return render(request,'login.html',{"message":"Invalid login credentials"})
    else:
        return render(request,'login.html')
    
    
class UserLogoutView(LogoutView):
    success_url = reverse_lazy("LoginView")
    

class Home(ListView):
    model=models.Reservation
    template_name="home.html"
    def get_queryset(self) -> QuerySet[Any]:
        user=self.request.user
        QuerySet=models.Reservation.objects.filter(user=user)
        return QuerySet
    def get_success_url(self):
        return reverse_lazy('home')


class ListFeedback(ListView):
    model=models.FeedbackModel
    context_object_name="feedback"
    template_name='chargingstationdetail.html'
    fields=['user','comment']

    def get_queryset(self) -> QuerySet[Any]:
        spot_id=self.kwargs.get('spot_id')
        return self.model.objects.filter(chargingspot_id=spot_id)


class ReservationListView(ListView):
    model=models.Reservation
    template_name="reservations.html"
    def get_queryset(self) -> QuerySet[Any]:
        user=self.request.user
        QuerySet=models.Reservation.objects.filter(user=user)
        return QuerySet
    

def ReservationDetailsView(request):
    return render(request, 'reservationdetails.html')

    
    
class ReservationDeleteView(DeleteView):
    model=models.Reservation
    success_url=reverse_lazy('ReservationListView')  
    template_name='reservations.html'
    
def select_place(request):
    locations = models.Location.objects.all()
    if request.method == 'POST':
        place_id = request.POST.get('place_name')
        return redirect('stationList', place_id=place_id)
    return render(request, 'stationinputselect.html', {'locations': locations})


def StationList(request, place_id):
    place = get_object_or_404(models.Location, pk=place_id)
    charging_spots = models.Chargingspot.objects.filter(place=place)
    feedback = models.FeedbackModel.objects.filter(chargingspot__in=charging_spots)
    return render(request, 'stationlist.html', {'charging_spots': charging_spots,'feedback':feedback.first})

def ReservationDetailsView(request, id):
    reservation = get_object_or_404(models.Reservation, id=id)

    if request.method == "POST":
        completed = request.POST.get('complete') == 'on'
        reservation.completed = completed
        reservation.save()
        feedback = models.FeedbackModel.objects.create(
            user=request.user, 
            chargingspot=reservation.chargingspot,
            comment=request.POST.get('feedback')
        )
        feedback.save()

        return HttpResponseRedirect(reverse('ReservationListView'))
    else:
        return render(request, 'reservationdetails.html', {"reservation": reservation})

    
def chargingspotDetails(request, chargingspot_id):
    chargingspot = get_object_or_404(models.Chargingspot, pk=chargingspot_id)
    feedbacks =models.FeedbackModel.objects.filter(chargingspot=chargingspot)
    return render(request, 'chargingstationdetail.html', {'chargingspot': chargingspot, 'feedbacks': feedbacks})

from django.shortcuts import render, get_object_or_404
from . import models 

def PlaceReservationView(request,chargingspot_id):
    chargingspot = get_object_or_404(models.Chargingspot, id=chargingspot_id)
    return render(request, 'reservestation.html',{'chargingspot':chargingspot})



def PlaceReservation(request):
    chargingspot = get_object_or_404(models.Chargingspot, id=request.POST.get('spotid'))
    if request.method == 'POST':
        user = User.objects.filter(username = request.user.username).first()
        starttime = request.POST.get('starttime')
        endtime = request.POST.get('endtime')
        reservation = models.Reservation.objects.create(
            user=user,
            starttime=starttime,
            endtime=endtime,
            chargingspot=chargingspot
        )

        place = get_object_or_404(models.Location, pk=request.POST.get('placeid'))
        charging_spots = models.Chargingspot.objects.filter(place=place)
        feedback = models.FeedbackModel.objects.filter(chargingspot__in=charging_spots)
        
        return render(request, 'stationlist.html', {'charging_spots': charging_spots, 'feedback': feedback.first() if feedback else None})

    
        


