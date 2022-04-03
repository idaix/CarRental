from django.shortcuts import render
from .models import Vehicle, VehicleImages
# Create your views here.

# DASHBOARD PAGE
def dashboard(request):
    vehicles = Vehicle.objects.filter(owned_by=request.user.id)
    vehicles_count = vehicles.count()
    for i in vehicles:
        print(i.id)
    context = {
        'vehicles':vehicles,
        'vehicles_count':vehicles_count,
    }
    return render(request, 'agency/dashboard.html', context=context)




# VEHICLE DETAILS
def vehicle_details(request, pk):
    vehicle = Vehicle.objects.get(pk=pk)
    print(vehicle.id)
    # get vehicle images 
    images = VehicleImages.objects.filter(belong_to=vehicle)
    context = {
        'vehicle': vehicle,
        'images': images,
    }
    return render(request, 'agency/vehicle.html', context=context)