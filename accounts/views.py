from django.shortcuts import render, redirect
from django.contrib.auth import login, get_user_model
from agency.forms import ProfileForm, UserUpdateForm

from agency.models import Agency
from setup.models import Commune, Wilaya
from .forms import RegisterForm

def register(request):
    if request.method =="POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user= form.save()
            login(request, user)
            return redirect('home')
    else:
        form = RegisterForm()
    
    context = {
        'form':form
    }
    return render(request, 'registration/register.html', context=context)



def profile(request):
    # THERE IS 3 TYPES OF PROFILES -AGENT- -ADMIN- -USER-
    user = request.user
    if request.user.is_agent:
        # AGNECY
        profile = Agency.objects.get(user=user)
        context = {
            'profile': profile,
        }
        return render(request, 'agency/profile.html', context=context)
    # elif request.user.is_superuser:
    #     context = {'user': user,}
    #     return render(request, 'accounts/profile.html', context=context)
    else:
        context = {'user': user,}
        return render(request, 'accounts/profile.html', context=context)


def profile_edit(request):
    # check
    if request.user.is_agent:
        # AGNECY
        if request.method == "POST":
            u_form = UserUpdateForm(request.POST, request.FILES, instance=request.user)
            p_form = ProfileForm(request.POST, request.FILES, instance=request.user.agency)
            if p_form.is_valid() and u_form.is_valid():
                u_form.save()
                agency = p_form.save(commit=False)
                # set agency address
                agency.wilaya=Wilaya.objects.get(id=request.POST.get('wilaya'))
                agency.commune=Commune.objects.get(id=request.POST.get('commune'))
                agency.state = agency.wilaya.name
                agency.city = agency.commune.name
                agency.save()
                return redirect('profile')
        else:
            u_form = UserUpdateForm(instance=request.user)
            p_form = ProfileForm(instance=request.user.agency)
        
        wilayas = Wilaya.objects.all()
        
        context = {
            'profile': request.user.agency,
            'u_form' : u_form,
            'p_form' : p_form,
            'wilayas' : wilayas,
        }
        return render(request, 'agency/profile_edit.html', context=context)
    else:
        user = request.user
        if request.method == "POST":
            u_form = UserUpdateForm(request.POST, request.FILES, instance=user)
            if u_form.is_valid():
                u_form.save()
                return redirect('profile')
        else:
            u_form = UserUpdateForm(instance=user)
        
        context = {'user': user,'u_form' : u_form}
        return render(request, 'accounts/profile_edit.html', context=context)
