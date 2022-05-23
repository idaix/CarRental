from django.urls import path
from . import views
from.views import MakeCreateView, MakeDeleteView, MakeUpdateView,ModelCreateView, ModelDeleteView, ModelUpdateView,EnergyCreateView,EnergyDeleteView,EnergyUpdateView,OptionCreateView,OptionDeleteView,OptionUpdateView,TransmissionCreateView,TransmissionDeleteView,TransmissionUpdateView,TypeCreateView,TypeDeleteView,TypeUpdateView,WilayaCreateView,WilayaDeleteView,WilayaUpdateView,CommuneCreateView,CommuneDeleteView,CommuneUpdateView
urlpatterns = [
    path('', views.dashboard, name='admin-dashboard'),
    path('users', views.manage_users, name='manage_users'),
    path('users/search', views.manage_users_search, name='manage_users_search'),
    path('users/all', views.manage_users_all, name='manage_users_all'),
    path('users/admin', views.manage_users_admin, name='manage_users_admin'),
    path('users/admin/add', views.manage_users_admin_add, name='manage_users_admin_add'),
    path('users/agency', views.manage_users_agency, name='manage_users_agency'),
    path('users/agency/add', views.manage_users_agency_add, name='manage_users_agency_add'),
    path('users/member', views.manage_users_member, name='manage_users_member'),
    path('users/member/add', views.manage_users_member_add, name='manage_users_member_add'),
    path('users/<int:pk>', views.manage_user, name='manage_user'),
    # messages
    path('messages/', views.v_messages, name='v_messages'),
    path('messages/<int:pk>', views.v_message_read, name='v_message_read'),
    # path('messages/<int:pk>/reply', views.v_message_reply, name='v_message_reply'),
    # setup
    path('setup', views.setup, name='setup'),
    path('make/new/', MakeCreateView.as_view(), name='make-create'),
    path('make/<int:pk>/update/', MakeUpdateView.as_view(), name='make-update'),
    path('make/<int:pk>/delete/', MakeDeleteView.as_view(), name='make-delete'),
    path('make/change', views.MakeChange, name='make-change'),

    path('model/new/', ModelCreateView.as_view(), name='model-create'),
    path('model/<int:pk>/update/', ModelUpdateView.as_view(), name='model-update'),
    path('model/<int:pk>/delete/', ModelDeleteView.as_view(), name='model-delete'),
    path('model/change/', views.ModelChange, name='model-change'),

    path('option/new/', OptionCreateView.as_view(), name='option-create'),
    path('option/<int:pk>/update/', OptionUpdateView.as_view(), name='option-update'),
    path('option/<int:pk>/delete/', OptionDeleteView.as_view(), name='option-delete'),
    path('option/change', views.OptionChange, name='option-change'),

    path('transmission/new/', TransmissionCreateView.as_view(), name='transmission-create'),
    path('transmission/<int:pk>/update/', TransmissionUpdateView.as_view(), name='transmission-update'),
    path('transmission/<int:pk>/delete/', TransmissionDeleteView.as_view(), name='transmission-delete'),
    path('transmission/change', views.TransmissionChange, name='transmission-change'),

    path('type/new/', TypeCreateView.as_view(), name='type-create'),
    path('type/<int:pk>/update/', TypeUpdateView.as_view(), name='type-update'),
    path('type/<int:pk>/delete/', TypeDeleteView.as_view(), name='type-delete'),
    path('type/change', views.TypeChange, name='type-change'),
    
    path('energy/new/', EnergyCreateView.as_view(), name='energy-create'),
    path('energy/<int:pk>/update/', EnergyUpdateView.as_view(), name='energy-update'),
    path('energy/<int:pk>/delete/', EnergyDeleteView.as_view(), name='energy-delete'),
    path('energy/change', views.EnergyChange, name='energy-change'),

    path('wilaya/new/', WilayaCreateView.as_view(), name='wilaya-create'),
    path('wilaya/<int:pk>/update/', WilayaUpdateView.as_view(), name='wilaya-update'),
    path('wilaya/<int:pk>/delete/', WilayaDeleteView.as_view(), name='wilaya-delete'),
    path('wilaya/change', views.WilayaChange, name='wilaya-change'),

    path('commune/new/', CommuneCreateView.as_view(), name='commune-create'),
    path('commune/<int:pk>/update/', CommuneUpdateView.as_view(), name='commune-update'),
    path('commune/<int:pk>/delete/', CommuneDeleteView.as_view(), name='commune-delete'),
    path('commune/change', views.CommuneChange, name='commune-change'),

]