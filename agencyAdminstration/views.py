from django.shortcuts import render
from .models import VehicleImages
# Create your views here.

# DASHBOARD PAGE
def dashboard(request):
    images = VehicleImages.objects.all()
    context = {
        'images':images
    }
    return render(request, 'agency/dashboard.html', context=context)