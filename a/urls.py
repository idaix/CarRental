from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='admin-dashboard'),
    path('users', views.manage_users, name='manage_users'),
    path('users/all', views.manage_users_all, name='manage_users_all'),
    path('users/admin', views.manage_users_admin, name='manage_users_admin'),
    path('users/agency', views.manage_users_agency, name='manage_users_agency'),
    path('users/member', views.manage_users_member, name='manage_users_member'),
    path('users/<int:pk>', views.manage_user, name='manage_user'),
]