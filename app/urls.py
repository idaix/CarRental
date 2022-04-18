from unicodedata import name
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('search/', views.search, name='search'),
    path('vehicle/<int:pk>', views.vehicle_details, name='vehicle_details'),
]