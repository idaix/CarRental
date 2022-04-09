from django.shortcuts import render, redirect
from .models import Vehicle, Images, Model, Make

from .forms import VehicleForm
from django.views.generic.edit import DeleteView
from django.urls import reverse_lazy

# Create your views here.

# VEHICLE DETAILS
def vehicle_details(request, pk):
    vehicle = Vehicle.objects.get(pk=pk)
    print(vehicle.id)
    # get vehicle images 
    images = Images.objects.filter(belong_to=vehicle)
    context = {
        'vehicle': vehicle,
        'images': images,
    }
    return render(request, 'vehicle/vehicle.html', context=context)

# ADD VEHICLE
def add_vehicle(request):
    if request.method == 'POST':
        form = VehicleForm(request.POST)
        if form.is_valid():
            # create the vehicle
            vehicle = form.save(commit=False)
            vehicle.owned_by = request.user
            vehicle.make=Make.objects.get(id=request.POST.get('make'))
            vehicle.model=Model.objects.get(id=request.POST.get('model'))
            vehicle.save()
            # Add images that belong to this vehicle
            # collect multiple images
            images = request.FILES.getlist('images')
            if images:
                for image in images:
                    new_image = Images(
                        belong_to = vehicle,
                        image = image
                    )
                    if new_image.save():
                        print('Done')
            # update thumbnail
                random_image = Images.objects.filter(belong_to=vehicle)[0]
                vehicle.thumbnail = random_image
                vehicle.save()
            return redirect('dashboard')
        
    else:
        form = VehicleForm()

    makes=Make.objects.all()
    context = {
        'form':form,
        'makes':makes
    }
    return render(request, 'vehicle/add_vehicle.html', context=context)

def model_field(request):
    if request.method == 'GET':
            
            models=Model.objects.filter(make = request.GET.get('make'))
            context={'models':models}
            return render(request, 'vehicle/partials/model_field.html', context=context)



# UPDATE VEHICLE
def update_vehicle(request, pk):
    vehicle = Vehicle.objects.get(pk=pk)
    if request.method == 'POST':
        form = VehicleForm(request.POST, instance=vehicle)
        if form.is_valid():
            form.save()
            images = request.FILES.getlist('images')
            for image in images:
                new_image = Images(
                    belong_to = vehicle,
                    image = image
                )
                if new_image.save():
                    print('Done')
            return redirect('dashboard')
    else:
        form = VehicleForm(instance=vehicle)
    
    context = {
        'form':form
    }
    return render(request, 'vehicle/update_vehicle.html', context=context)


class VehicleDelete(DeleteView):
    model = Vehicle
    success_url = reverse_lazy('dashboard')
