from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from app.forms import ClientForm
from setup.models import Commune, Wilaya
from vehicle.models import Images, Vehicle, Type, Energy, Transmission
from agency.models import Agency
from order.models import Order
from django.db.models import Q
from datetime import datetime

# Create your views here.

def home(request):
    wilayas = Wilaya.objects.all()
    context = {
        'wilayas': wilayas,
    }
    return render(request, 'app/home.html', context)


# SEARCH FORM
def search(request):

    # Quique check if city selected
    if request.GET.get('commune'):
        state = Wilaya.objects.get(id=request.GET.get('wilaya'))
        city = Commune.objects.get(id=request.GET.get('commune'))
        date_start = request.GET.get('date-start', '')
        date_end = request.GET.get('date-end', '')
    else:
        return redirect('home')

    result=[]
    agencies = Agency.objects.filter(commune=city)
    for agency in agencies:
        if agency.get_available_cars_count()>0:
            result.append(agency)
    # result = Agency.objects.filter(Q(state__icontains=city) | Q(city__icontains=city) | Q(address__icontains=city))
    # for sidebar...
    types = Type.objects.all()
    energy = Energy.objects.all()
    transmission = Transmission.objects.all()
    wilayas = Wilaya.objects.all()
    context = {
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
    context = {
        'agency':agency,
        'cars':cars,
        'city':city,
        'date_start':date_start,
        'date_end':date_end,
        'types':types,
        'energy':energy,
        'transmission':transmission,
    }
    return render(request, 'app/search/show_all_cars.html', context=context)


# VEHICLE DETAIL 
def vehicle_details(request, pk):
    vehicle = Vehicle.objects.get(pk=pk)
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
            order = Order.objects.get(pk=int(number))
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


