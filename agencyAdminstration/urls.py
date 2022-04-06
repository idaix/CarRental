from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('add_vehicle/', views.add_vehicle, name='add_vehicle'),
    path('model_field/', views.model_field, name='model_field'),
    path('vehicle/<int:pk>', views.vehicle_details, name='vehicle_details'),
    path('vehicle/<int:pk>/update', views.update_vehicle, name='vehicle_update'),
    path('vehicle/<int:pk>/delete', views.VehicleDelete.as_view(), name='vehicle_delete'),
]