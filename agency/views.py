from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.views.generic.edit import UpdateView
from .forms import ProfileForm, RegisterForm, UserUpdateForm, VehicleForm
from vehicle.models import Make, Model, Vehicle, Images
from .models import Agency
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import DeleteView
from django.urls import reverse_lazy


# Agency Registration ...
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            # login user
            login(request, user)
            agency = Agency.objects.create(user=user ,name=user.username)
            return redirect('agency_profile')
    else:
        form = RegisterForm()
    

    context = {
        'form' : form
    }

    return render(request, 'agency/register.html', context=context)


# Agency Agency Show...
@login_required
def agency_profile(request):
    profile = Agency.objects.get(user=request.user)
    context = {
        'profile': profile,
    }
    return render(request, 'agency/profile.html', context=context)
# Edit profile
@login_required
def agency_profile_edit(request):
    profile = Agency.objects.get(user=request.user)
    if request.method == "POST":
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileForm(request.POST, request.FILES, instance=profile)
        if p_form.is_valid() and u_form.is_valid():
            u_form.save()
            p_form.save()
            return redirect('agency_profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileForm(instance=profile)
    context = {
        'profile': profile,
        'u_form' : u_form,
        'p_form' : p_form,
    }
    return render(request, 'agency/profile_edit.html', context=context)


# Agency Edit ... (i used UpdateView)
class AgencyUpdateView(UpdateView):
    model = Agency
    fields = ['name', 'image', 'contact_phone', 'contact_website', 'location']

# DASHBOARD PAGE
@login_required
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


# VEHICLE PART==================================================================
# vehcile details...
@login_required
def vehicle_details(request, pk):
    vehicle = Vehicle.objects.get(pk=pk)
    # get vehicle images 
    images = Images.objects.filter(belong_to=vehicle)
    context = {
        'vehicle': vehicle,
        'images': images,
    }
    return render(request, 'vehicle/vehicle.html', context=context)

# ADD VEHICLE
@login_required
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
@login_required
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



