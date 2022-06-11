from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('contact/', views.contact_page, name='contact_page'),
    path('about/', views.about_page, name='about_page'),
    path('search/', views.search, name='search'),
    path('search/<int:pk>', views.show_all_cars, name='show_all_cars'),
    path('vehicle/<int:pk>', views.vehicle_details, name='vehicle_details'),
    # Booking
    path('book/<int:pk>', views.book, name='book'),
    path('book/confirm_reservation/<int:pk>', views.confirm_reservation, name='confirm_reservation'),
    path('book/manage_booking', views.manage_booking, name='manage_booking'),
    # FEEDBACKS
    path('create_feedback/', views.CreateFeedback, name='create_feedback'),
    path('delete_feedback/<int:pk>', views.DeleteFeedback, name='delete_feedback'),
    # send message to admin
    path('send_message_to_admin/', views.send_message_to_admin, name='send_message_to_admin'),

]