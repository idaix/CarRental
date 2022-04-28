from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('search/', views.search, name='search'),
    path('search/<int:pk>', views.show_all_cars, name='show_all_cars'),
    path('vehicle/<int:pk>', views.vehicle_details, name='vehicle_details'),
    # Booking
    path('book/<int:pk>', views.book, name='book'),
]