from distutils.log import error
import json
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.core import serializers
from a.models import HelpMessage
from app.forms import ClientForm
from feedbacks.forms import FeedbackForm
from feedbacks.models import feedback
from setup.models import Commune, Wilaya
from vehicle.models import Images, Vehicle, Type, Energy, Transmission
from agency.models import Agency
from order.models import Order
from django.db.models import Q
from datetime import datetime
from django.contrib.auth.decorators import login_required
import random

# Create your views here.

def home(request):
    wilayas = Wilaya.objects.all()
    popular_detinations = Commune.objects.all()[:6]
    faq = list(HelpMessage.objects.filter(is_replied=True))
    if len(faq)>4:
        faq = random.sample(faq, 4)
    
    context = {
        'wilayas': wilayas,
        'popular_detinations': popular_detinations,
        'faq': faq,
    }
    return render(request, 'app/home.html', context)


# SEARCH FORM
def search(request):

    print(request.GET)
    # Quique check if city selected
    if request.GET.get('commune'):
        state = Wilaya.objects.get(id=request.GET.get('wilaya'))
        city = Commune.objects.get(id=request.GET.get('commune'))
        date_start = request.GET.get('date-start', '')
        date_end = request.GET.get('date-end', '')
    else:
        return redirect('home')
    
    if city:
        city.update_views()
        city.save()

    # GET RESULT------------------
    result=[]
    agencies = Agency.objects.filter(commune=city)
    for agency in agencies:
        if agency.get_available_cars_count()>0:
            result.append(agency)
    # GET RESULT------------------
    # for sidebar...
    # MAP---
    geocode = city.longitude, city.latitude
    types = Type.objects.all()
    energy = Energy.objects.all()
    transmission = Transmission.objects.all()
    wilayas = Wilaya.objects.all()


    # this data used to show agencies in map 
    # data = {}
    # data = serializers.serialize('json', result)
    # data = json.dumps(agencies)
    context = {
        'geocode':geocode,
        'wilayas':wilayas,
        'result':result,
        'city':city,
        'state':state,
        'date_start':date_start,
        'date_end':date_end,
        'types':types,
        'energy':energy,
        'transmission':transmission,
    }
    return render(request, 'app/search/search.html', context=context)
# SHOW ALL CARS FOR SPESIFIC AGENCY
def show_all_cars(request, pk):
    agency = Agency.objects.get(pk=pk)
    # comments
    comments=feedback.objects.filter(agency=pk)
    form= FeedbackForm()
    # update vehicle viewes count
    agency.update_views()
    agency.save()
    # Show only available vehicles
    cars = Vehicle.objects.filter(owned_by=agency).filter(is_available=True)
    # from get
    city = request.GET.get('city', '')
    date_start = request.GET.get('date-start', '')
    date_end = request.GET.get('date-end', '') 
    # for sidebar...
    types = Type.objects.all()
    energy = Energy.objects.all()
    transmission = Transmission.objects.all()

    # FILTER
    if request.POST:
        if request.POST.get('type'):
            _type= Type.objects.get(id=request.POST.get('type'))
            cars=cars.filter(type=_type)
        if request.POST.get('energy'): 
            _energy= Energy.objects.get(id=request.POST.get('energy'))
            cars=cars.filter(engine=_energy)
        if request.POST.get('transmission'):
            _transmission= Transmission.objects.get(id=request.POST.get('transmission'))
            cars=cars.filter(transmission=_transmission)
    context = {
        'agency':agency,
        'cars':cars,
        'city':city,
        'date_start':date_start,
        'date_end':date_end,
        'types':types,
        'energy':energy,
        'transmission':transmission,
        'comments':comments,
        'form':form,
    }
    return render(request, 'app/search/show_all_cars.html', context=context)


# VEHICLE DETAIL 
def vehicle_details(request, pk):
    vehicle = Vehicle.objects.get(pk=pk)
    # update vehicle viewes count
    vehicle.update_views()
    vehicle.save()
    # get vehicle images 
    images = Images.objects.filter(belong_to=vehicle)
    context = {
        'vehicle': vehicle,
        'images': images,
    }
    return render(request, 'app/vehicle.html', context=context)


# ORDER
def book(request, pk):
    date_start = request.GET.get('date-start', '')
    date_end = request.GET.get('date-end', '')
    if not date_start:date_start = datetime.today()
    if not date_end:date_end = datetime.today()

    car = Vehicle.objects.get(pk=pk)
    agency = car.owned_by
    if request.method == 'POST':
        client_form = ClientForm(request.POST)
        if client_form.is_valid():
            # create client
            client = client_form.save(commit=False)
            client.agency = agency
            client = client_form.save()
            # create client order
            order = Order(
                vehicle=car,
                agency=agency,
                client=client,
                date_start=date_start,
                date_end=date_end,
                price=car.price,
            )
            order.save()
            # client = order.client
            # vehicle = order.vehicle
            # context = {
            #         'order': order,
            #         'client': client,
            #         'vehicle': vehicle
            # }
            # return render(request, 'app/booking/confirm_reservation.html', context=context) //NOT WORKING!!
            return redirect('confirm_reservation', pk=order.id)
    else:
        client_form = ClientForm()
    
    context = {
        'date_start':date_start,
        'date_end':date_end,
        'car': car,
        'agency': agency,
        'client_form': client_form,
    }

    return render(request, 'app/booking/book.html', context)




# confirm_reservation
def confirm_reservation(request, pk):
    order = Order.objects.get(pk=pk)
    client = order.client
    vehicle = order.vehicle
    context = {
        'order': order,
        'client': client,
        'vehicle': vehicle
    }
    return render(request, 'app/booking/order_detail.html', context=context)

# MANAGE BOOKING
def manage_booking(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        number = request.POST.get('number')
        # check if empty
        if not email or not number:
            return redirect('home')
        else:
            # get unique order
            try: order = Order.objects.get(pk=int(number))
            except: return redirect('home')
            client = order.client
            vehicle = order.vehicle
            # check if this order awned by this email
            if order.client.email == email:
                context = {
                    'order': order,
                    'client': client,
                    'vehicle': vehicle
                }
                return render(request, 'app/booking/order_detail.html', context=context)
            else:
                return redirect('home')

    else:
        if request.order:
            return redirect('login')
        else:
            return redirect('home')


#FEEDBACKS
@login_required
def CreateFeedback(request):
    
    if request.method=='POST':
        form=FeedbackForm(request.POST)
        if form.is_valid():
            feedback=form.save(commit=False)
            feedback.client=request.user
            agency=Agency.objects.get(id=request.GET.get('agency_id'))
            feedback.agency=agency
            feedback.save()
            return redirect('show_all_cars',agency.id)
    
    return render(request, 'app/search/show_all_cars.html')


@login_required
def DeleteFeedback(request,pk):
    id=feedback.objects.get(id=pk).agency.id
    
    if request.method=='GET':
        comment=feedback.objects.get(id=pk)
        if request.user.id==comment.client.id:
            comment.delete()
    return redirect('show_all_cars',id)






def send_message_to_admin(request):

    if request.method == 'POST':
        email = request.POST.get('email')
        message = request.POST.get('message')

        if email and message:
            m = HelpMessage.objects.create(email=email, message=message)
            m.save()
            return redirect('home')
        else:
            return redirect('home')
    else:
        return redirect('home')