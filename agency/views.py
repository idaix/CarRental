from pyexpat import model
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.views.generic.edit import UpdateView

from order.models import Order, Client
from .forms import ProfileForm, RegisterAgencyForm, RegisterUserForm, UserUpdateForm, VehicleForm
from vehicle.models import Make, Model, Vehicle, Images
from .models import Agency
from setup.models import Wilaya, Commune
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import DeleteView
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib import messages



# Agency Registration ...
def register(request):
    if request.method == 'POST':
        user_form = RegisterUserForm(request.POST)
        agency_form = RegisterAgencyForm(request.POST)
        if user_form.is_valid() and agency_form.is_valid():
            user = user_form.save(commit=False)
            user.is_agent = True
            user.save()
            agency = agency_form.save(commit=False)
            agency.user = user
            # set agency address
            agency.wilaya=Wilaya.objects.get(id=request.POST.get('wilaya'))
            agency.commune=Commune.objects.get(id=request.POST.get('commune'))
            agency.state = agency.wilaya.name
            agency.city = agency.commune.name
            agency.save()
            # login user
            login(request, user)
            msg = f'Account created, Please confirm your email'
            messages.success(request, msg)
            return redirect('profile')
    else:
        user_form = RegisterUserForm()
        agency_form = RegisterAgencyForm()

    wilayas = Wilaya.objects.all()

    context = {
        'user_form' : user_form,
        'agency_form' : agency_form,
        'wilayas' : wilayas,
    }

    return render(request, 'agency/register.html', context=context)
def commune_field(request):
    if request.method == 'GET':
            commune=Commune.objects.filter(wilaya_id = request.GET.get('wilaya'))
            context={'commune':commune}
            return render(request, 'location/partials/commune_field.html', context=context)

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
        u_form = UserUpdateForm(request.POST, request.FILES, instance=request.user)
        p_form = ProfileForm(request.POST, request.FILES, instance=profile)
        if p_form.is_valid() and u_form.is_valid():
            u_form.save()
            agency = p_form.save(commit=False)
            # set agency address
            agency.wilaya=Wilaya.objects.get(id=request.POST.get('wilaya'))
            agency.commune=Commune.objects.get(id=request.POST.get('commune'))
            agency.state = agency.wilaya.name
            agency.city = agency.commune.name
            agency.save()

            msg = f"Changes saved."
            messages.success(request, msg)
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileForm(instance=profile)
    
    wilayas = Wilaya.objects.all()
    
    context = {
        'profile': profile,
        'u_form' : u_form,
        'p_form' : p_form,
        'wilayas' : wilayas,
    }
    return render(request, 'agency/profile_edit.html', context=context)


# Agency Edit ... (i used UpdateView)
# class AgencyUpdateView(UpdateView):
#     model = Agency
#     fields = ['name', 'image', 'contact_phone', 'contact_website', 'location']

# DASHBOARD PAGE
@login_required
def dashboard(request):
    if request.user.is_agent or request.user.is_staff:
        vehicles = Vehicle.objects.filter(owned_by=request.user.agency)
        vehicles_count = vehicles.count()
        orders = Order.objects.filter(agency=request.user.agency)
        orders_3 = orders[:3]
        orders_count = orders.count()
        clients = orders.filter(status='a')[:3]
        clients_count = orders.filter(status='a').count()
        
        context = {
            'views_count':request.user.agency.views,
            'vehicles':vehicles,
            'vehicles_count':vehicles_count,
            'orders':orders_3,
            'orders_count':orders_count,
            'clients':clients,
            'clients_count':clients_count,
        }
    else:
        return redirect('home')
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
        print(request.POST)
        if form.is_valid():
            # create the vehicle
            vehicle = form.save(commit=False)
            vehicle.owned_by = request.user.agency
            vehicle.make=Make.objects.get(id=request.POST.get('make'))
            vehicle.model=Model.objects.get(id=request.POST.get('model'))
            vehicle.save()
            form.save_m2m()
            # Add images that belong to this vehicle
            # collect multiple images
            images = request.FILES.getlist('images')
            if images:
                for image in images:
                    new_image = Images(
                        belong_to = vehicle,
                        image = image
                    )
                    new_image.save()
                # update thumbnail
                random_image = Images.objects.filter(belong_to=vehicle)[0]
                vehicle.thumbnail = random_image
                vehicle.save()
            else:pass
            msg = f'{vehicle.get_title()} successfully added'
            messages.success(request, msg)
            return redirect('dashboard')
        else:
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
            models=Model.objects.filter(make_id = request.GET.get('make'))
            context={'models':models}
            return render(request, 'vehicle/partials/model_field.html', context=context)

# UPDATE VEHICLE
@login_required
def update_vehicle(request, pk):
    vehicle = Vehicle.objects.get(pk=pk)
    images = Images.objects.filter(belong_to=vehicle)
    makes = Make.objects.all()
    if request.method == 'POST':
        print(request.POST)
        form = VehicleForm(request.POST, instance=vehicle)
        if form.is_valid():
            vehicle = form.save(commit=False)
            vehicle.make=Make.objects.get(id=request.POST.get('make'))
            vehicle.model=Model.objects.get(id=request.POST.get('model'))
            vehicle.save()
            form.save_m2m()
            images = request.FILES.getlist('images')
            for image in images:
                new_image = Images(
                    belong_to = vehicle,
                    image = image
                )
                if new_image.save():
                    print('Done')
            msg = f'{vehicle.get_title()} successfully updated.'
            messages.success(request, msg)
            return redirect('dashboard')
    else:
        form = VehicleForm(instance=vehicle)
    
    context = {
        'form':form,
        'images':images,
        'vehicle':vehicle,
        'makes':makes,
    }
    return render(request, 'vehicle/update_vehicle.html', context=context)

def update_model_field(request,pk):
    vehicle=Vehicle.objects.get(pk=pk)
    models=Model.objects.filter(make_id=vehicle.make)
    
    if request.method == 'GET':
        models=Model.objects.filter(make_id = request.GET.get('make'))
    context={'models':models,'vehicle':vehicle}
    return render(request, 'vehicle/partials/update_model_field.html', context=context)

# delete vehicle

# def delete_vehicle(request, pk):
#     car = Vehicle.objects.get(pk=pk)
#     car_name = car.get_title()
#     if car.delete():
#         msg = f'{car_name } was deleted successfully.'
#         messages.success(request, msg)
#     return redirect('dashboard')

class VehicleDelete(DeleteView):
    model = Vehicle
    success_url = reverse_lazy('dashboard')
    success_message = "Car was deleted successfully."

def update_vehicle_image(request, pk, pk_img):
    img = Images.objects.get(pk=pk_img)
    img.delete()
    return redirect('vehicle_update', pk=pk)
# change status
@login_required
def change_status_vehicle(request, pk):
    car = Vehicle.objects.get(pk=pk)
    # check the curen status
    if car.is_available:
        car.is_available = False
        car.save()
        msg = f'{car.get_title()} disabled.'
    else:
        car.is_available = True
        car.save()
        msg = f'{car.get_title()} enabled.'
        
    messages.success(request, msg)
    return redirect('dashboard')


# Accept, refuse orders
@login_required
def accept_order(request, pk):
    order = Order.objects.get(pk=pk)
    vehicle = order.vehicle
    return_to = request.GET.get('return_to')
    if order.is_available:
        if vehicle.is_available:
            order.is_available = False
            order.status = 'a'
            vehicle.is_available = False
            vehicle.save()
            order.save()
    if return_to == 'dashboard':
        msg = f"You have accepted {order.client.get_full_name()}."
        messages.success(request, msg)
        return redirect(return_to)
    else:
        return redirect(return_to, pk=pk)
    
def refuse_order(request, pk):
    order = Order.objects.get(pk=pk)
    vehicle = order.vehicle
    return_to = request.GET.get('return_to')
    if order.is_available:
        order.is_available = False
        order.status = 'r'
        order.save()
    return redirect(return_to, pk=pk)



# garage 
@login_required
def garage(request):
    vehicles = Vehicle.objects.filter(owned_by=request.user.agency)
    vehicles_count = vehicles.count()
    context = {
        'vehicles':vehicles,
        'vehicles_count':vehicles_count,
    }
    return render(request, 'agency/dashboard.html', context=context)

# orders 
@login_required
def orders(request):
    orders = Order.objects.filter(agency=request.user.agency)
    orders_count = orders.count()
    context = {
        'orders':orders,
        'orders_count':orders_count,
    }
    return render(request, 'order/orders.html', context=context)

# clients 
@login_required
def clients(request):
    orders = Order.objects.filter(agency=request.user.agency).filter(status='a')
    
    clients = orders
    clients_count = orders.count()
    
    context = {
        'clients':clients,
        'clients_count':clients_count,
    }
    return render(request, 'client/clients.html', context=context)

@login_required
def order_detail(request, pk):
    order = Order.objects.get(pk=pk)
    client = order.client
    vehicle = order.vehicle
    context = {
        'order':order,
        'client':client,
        'vehicle':vehicle,
    }
    return render(request, 'order/order_detail.html', context=context)