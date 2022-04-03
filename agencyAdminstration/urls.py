from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('vehicle/<int:pk>', views.vehicle_details, name='vehicle_details'),
]