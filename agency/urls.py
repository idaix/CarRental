from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='agency_register'),
    path('profile/', views.agency_profile, name='agency_profile'),
    path('profile/edit', views.agency_profile_edit, name='agency_profile_edit'),
    path('profile/edit/<int:pk>', views.AgencyUpdateView.as_view(), name='agency_profile_edit'),
    path('dashboard/', views.dashboard, name='dashboard'),
    # AGENCY VEHICLE URLS
    path('vehicle/<int:pk>', views.vehicle_details, name='agency_vehicle_details'),
    path('vehicle/add_vehicle/', views.add_vehicle, name='add_vehicle'),
    path('vehicle/model_field/', views.model_field, name='model_field'),
    path('vehicle/<int:pk>/update', views.update_vehicle, name='vehicle_update'),
    path('vehicle/<int:pk>/delete', views.VehicleDelete.as_view(), name='vehicle_delete'),
]