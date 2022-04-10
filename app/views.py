from django.shortcuts import render
from vehicle.models import Vehicle
# Create your views here.

def home(request):
    vehicles = Vehicle.objects.all()
    context = {
        'vehicles': vehicles
    }
    return render(request, 'app/home.html', context)