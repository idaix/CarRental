from django.shortcuts import render
from vehicle.models import Images, Vehicle, Type, Energy, Transmission
from agency.models import Agency
from django.db.models import Q

# Create your views here.

def home(request):
    vehicles = Vehicle.objects.all()
    context = {
        'vehicles': vehicles
    }
    return render(request, 'app/home.html', context)


# SEARCH FORM
def search(request):
    city = request.GET.get('city', '')
    date_start = request.GET.get('date-start', '')
    date_end = request.GET.get('date-end', '')
    agencies = Agency.objects.filter(Q(state__icontains=city) | Q(city__icontains=city) | Q(address__icontains=city))
    # for sidebar...
    types = Type.objects.all()
    energy = Energy.objects.all()
    transmission = Transmission.objects.all()
    context = {
        'agencies':agencies,
        'city':city,
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

