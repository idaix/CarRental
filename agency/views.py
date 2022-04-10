from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.views.generic.edit import UpdateView
from .forms import ProfileForm, RegisterForm, UserUpdateForm
from vehicle.models import Vehicle
from .models import Agency
from django.contrib.auth.decorators import login_required
# Create your views here.
# Agency Registration ...
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            # login user
            login(request, user)
            agency = Agency.objects.create(user=user ,name=user.username)
            return redirect('dashboard')
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

    return render(request, 'agency/profile.html', context=context)


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





