from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm

def register(request):
    if request.method =="POST":
        form = UserCreationForm(request.POST)
        if form.is_valid:
            user= form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    
    context = {
        'form':form
    }
    return render(request, 'registration/register.html', context=context)
