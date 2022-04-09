from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='agency_register'),
    path('profile/', views.agency_profile, name='agency_profile'),
    path('profile/edit/<int:pk>', views.AgencyUpdateView.as_view(), name='agency_profile_edit'),
    path('dashboard/', views.dashboard, name='dashboard'),
]