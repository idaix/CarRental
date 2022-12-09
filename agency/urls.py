from django.urls import path
from . import views

urlpatterns = [
    # AGENCY REGISTRATION
    path('register/', views.register, name='agency_register'),
    path('commune_field/', views.commune_field, name='commune_field'),
    # AGENCY PROFILE
    # path('profile/', views.agency_profile, name='agency_profile'),
    # path('profile/edit', views.agency_profile_edit, name='agency_profile_edit'),
    # path('profile/edit/<int:pk>', views.AgencyUpdateView.as_view(), name='agency_profile_edit'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/plan', views.my_plan, name='myplan'),
    # AGENCY VEHICLE URLS
    path('vehicle/<int:pk>', views.vehicle_details, name='agency_vehicle_details'),
    path('vehicle/add_vehicle/', views.add_vehicle, name='add_vehicle'),
    path('vehicle/model_field/', views.model_field, name='model_field'),
    path('vehicle/<int:pk>/update', views.update_vehicle, name='vehicle_update'),
    path('vehicle/<int:pk>/update_model_field', views.update_model_field, name='update_model_field'),
    path('vehicle/<int:pk>/update/image/<int:pk_img>', views.update_vehicle_image, name='vehicle_update_image'),
    path('vehicle/<int:pk>/change_status', views.change_status_vehicle, name='change_status_vehicle'),
    # path('vehicle/<int:pk>/delete', views.delete_vehicle, name='vehicle_delete'),
    path('vehicle/<int:pk>/delete', views.VehicleDelete.as_view(), name='vehicle_delete'),
    # AGENCY ORDERS URLS
    path('orders/', views.orders, name='orders'),
    path('order/<int:pk>/', views.order_detail, name='order_detail'),
    path('order/<int:pk>/accept', views.accept_order, name='accept_order'),
    path('order/<int:pk>/refuse', views.refuse_order, name='refuse_order'),
    # AGENCY CLIENTS URLS
    path('clients/', views.clients, name='clients'),
]