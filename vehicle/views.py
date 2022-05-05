from django.shortcuts import render, redirect
from .models import Vehicle, Images, Model, Make

from .forms import VehicleForm
from django.views.generic.edit import DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
# Create your views here.
