from multiprocessing import context
from django.shortcuts import render, redirect
from django.contrib.admin.views.decorators import staff_member_required
from a.models import HelpMessage
from accounts.models import User
from django.db.models import Q
from a.forms import ReolyToMessageForm
from django.urls import reverse_lazy
from vehicle.models import Make,Model,Option,Type,Energy,Transmission
from setup.models import Wilaya,Commune
from django.views.generic import (
    CreateView,
    UpdateView,
    DeleteView,
    ListView,
)


import agency
from .forms import AdminForm, AgencyForm, AgencyFormCreate, UserForm
# Create your views here.
@staff_member_required()
def dashboard(request):
    return render(request, 'a/dashboard.html')
@staff_member_required()
def manage_users(request):
    if request.user.is_staff:
        # App users-------------------------------
        users = User.objects.all()
        users_only_3 = users[:3]
        admins = users.filter(is_staff = True)[:3]
        admins_count = users.filter(is_staff = True).count()
        agencies = users.filter(is_agent = True)[:3]
        agencies_count = users.filter(is_agent = True).count()
        members = users.filter(is_agent = False)[:3]
        members_count = users.filter(is_agent = False).count()
        # ----------------------------------------

        context={
            'users': users,
            'users_only_3': users_only_3,
            'admins': admins,
            'admins_count': admins_count,
            'agencies': agencies,
            'agencies_count': agencies_count,
            'members': members,
            'members_count': members_count,
        }
    else:
        # don't have permission
        return redirect('home')
    return render(request, 'a/manage_users.html', context)
@staff_member_required()
def manage_users_search(request):
    if request.method == 'GET':
        q=request.GET.get('search', ' ')
        result = User.objects.filter(Q(username__icontains=q))
        context={'result':result}
    
    return render(request, 'a/users/search.html', context)
@staff_member_required()
def manage_users_all(request):
    if request.user.is_staff:
        users = User.objects.all()
        context={
            'users': users,
        }
    else:
        # don't have permission
        return redirect('home')
    
    return render(request, 'a/users/users.html', context)
@staff_member_required()
def manage_users_admin(request):
    if request.user.is_staff:
        users = User.objects.filter(is_staff = True)
        context={
            'users': users,
        }
    else:
        # don't have permission
        return redirect('home')
    
    return render(request, 'a/users/admin.html', context)
@staff_member_required()
def manage_users_agency(request):
    if request.user.is_staff:
        users = User.objects.filter(is_agent = True)
        context={
            'users': users,
        }
    else:
        # don't have permission
        return redirect('home')
    
    return render(request, 'a/users/agency.html', context)
@staff_member_required()
def manage_users_member(request):
    if request.user.is_staff:
        users = User.objects.filter(is_agent = False)
        context={
            'users': users,
        }
    else:
        # don't have permission
        return redirect('home')
    
    return render(request, 'a/users/member.html', context)
@staff_member_required()
def manage_user(request, pk):
    u = User.objects.get(pk=pk)
    if request.method=="POST":
        u_form = UserForm(request.POST, instance=u)
        if u_form.is_valid():
            u_form.save()
            if u.is_agent:
                a_form = AgencyForm(request.POST, instance=u.agency)
                if a_form.is_valid():
                    a_form.save()
                else:
                    return redirect('admin-dashboard')
        else:
            return redirect('admin-dashboard')
        
                
    else:
        u_form = UserForm(instance=u)
        if u.is_agent:a_form = AgencyForm(instance=u.agency)
    
    if u.is_agent:
        context={'u':u,'u_form':u_form,'a_form':a_form}
    else:
        context={'u':u,'u_form':u_form}
    return render(request, 'a/users/user_detail.html', context)
@staff_member_required()
def manage_users_admin_add(request):
    if request.method == 'POST':
        form = AdminForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_staff = True
            user.is_superuser = True
            user.save()
            return redirect('manage_users_admin')
    else:
        form = AdminForm()
    context={'u_form':form}
    return render(request, 'a/users/add.html', context)
@staff_member_required()
def manage_users_agency_add(request):
    if request.method == 'POST':
        u_form = AdminForm(request.POST)
        a_form = AgencyFormCreate(request.POST)
        if u_form.is_valid() and a_form.is_valid():
            user = u_form.save(commit=False)
            user.is_agent = True
            user.save()
            agency = a_form.save(commit=False)
            agency.user = user
            agency.save()
            return redirect('manage_users_agency')
    else:
        u_form = AdminForm()
        a_form = AgencyFormCreate()
    context={'u_form':u_form, 'a_form':a_form}
    return render(request, 'a/users/add.html', context)
@staff_member_required()
def manage_users_member_add(request):
    if request.method == 'POST':
        form = AdminForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('manage_users_member')
    else:
        form = AdminForm()
    context={'u_form':form}
    return render(request, 'a/users/add.html', context)

# Messages
def v_messages(request):
    messages = HelpMessage.objects.all()
    context={'messages':messages}
    return render(request, 'a/messages.html', context)

def v_message_read(request, pk):
    m = HelpMessage.objects.get(pk=pk)
    if request.method == 'POST':
        form = ReolyToMessageForm(request.POST, instance=m)
        if form.is_valid():
            message = form.save(commit=False)
            message.is_replied = True
            message.update_date()
            message.save()
            return redirect('v_message_read', pk=pk)
    else:
        form = ReolyToMessageForm(instance=m)
    context={'m':m, 'form':form}
    return render(request, 'a/messages/read.html', context)


# SETUP PART
@staff_member_required()
def setup(request):
    return render(request, 'a/setup.html')

##########################

class MakeCreateView(CreateView):
    model = Make
    fields = ['name']

class MakeDeleteView(DeleteView):
    model = Make
    success_url = reverse_lazy('make-change')

class MakeUpdateView(UpdateView):
    model = Make
    fields = ['name']

    def test_func(self):
        make = self.get_object()
        return True


# def MakeChange(request):
#     makes = Make.objects.all()
#     context = {
#         'makes':makes,
#     }
#     return render(request, 'vehicle/make_change.html', context)

class MakeListView(ListView):
    model = Make
    template_name = 'vehicle/make_change.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'makes'
    paginate_by = 8



#######################

class ModelCreateView(CreateView):
    model = Model
    fields = ['make_id','name','series']

class ModelDeleteView(DeleteView):
    model = Model
    success_url = reverse_lazy('model-change')

class ModelUpdateView(UpdateView):
    model = Model
    fields = ['make_id','name','series']

    def test_func(self):
        model = self.get_object()
        return True

# def ModelChange(request):
#     models = Model.objects.all()
#     context = {
#         'models':models,
#     }
#     return render(request, 'vehicle/model_change.html', context)

class ModelListView(ListView):
    model = Make
    template_name = 'vehicle/model_change.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'models'
    paginate_by = 8



###########################
class OptionCreateView(CreateView):
    model = Option
    fields = ['name']

class OptionDeleteView(DeleteView):
    model = Option
    success_url = reverse_lazy('option-change')

class OptionUpdateView(UpdateView):
    model = Option
    fields = ['name']

    def test_func(self):
        Option = self.get_object()
        return True


# def OptionChange(request):
#     Options = Option.objects.all()
#     context = {
#         'options':Options,
#     }
#     return render(request, 'vehicle/option_change.html', context)

class OptionListView(ListView):
    model = Option
    template_name = 'vehicle/option_change.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'options'
    paginate_by = 8


###########################
class TypeCreateView(CreateView):
    model = Type
    fields = ['name']

class TypeDeleteView(DeleteView):
    model = Type
    success_url = reverse_lazy('type-change')

class TypeUpdateView(UpdateView):
    model = Type
    fields = ['name']

    def test_func(self):
        Type = self.get_object()
        return True


# def TypeChange(request):
#     types = Type.objects.all()
#     context = {
#         'types':types,
#     }
#     return render(request, 'vehicle/type_change.html', context)

class TypeListView(ListView):
    model = Type
    template_name = 'vehicle/type_change.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'types'
    paginate_by = 8


###########################
class EnergyCreateView(CreateView):
    model = Energy
    fields = ['name']

class EnergyDeleteView(DeleteView):
    model = Energy
    success_url = reverse_lazy('energy-change')

class EnergyUpdateView(UpdateView):
    model = Energy
    fields = ['name']

    def test_func(self):
        Energy = self.get_object()
        return True


# def EnergyChange(request):
#     Energys = Energy.objects.all()
#     context = {
#         'energys':Energys,
#     }
#     return render(request, 'vehicle/energy_change.html', context)

class EnergyListView(ListView):
    model = Energy
    template_name = 'vehicle/energy_change.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'energys'
    paginate_by = 8


#######################
class TransmissionCreateView(CreateView):
    model = Transmission
    fields = ['name']

class TransmissionDeleteView(DeleteView):
    model = Transmission
    success_url = reverse_lazy('transmission-change')

class TransmissionUpdateView(UpdateView):
    model = Transmission
    fields = ['name']

    def test_func(self):
        transmission = self.get_object()
        return True


# def TransmissionChange(request):
#     Transmissions = Transmission.objects.all()
#     context = {
#         'transmissions':Transmissions,
#     }
#     return render(request, 'vehicle/transmission_change.html', context)

class TransmissionListView(ListView):
    model = Transmission
    template_name = 'vehicle/transmission_change.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'transmissions'
    paginate_by = 8

#######################
class WilayaCreateView(CreateView):
    model = Wilaya
    fields = ['code','name','ar_name','longitude','latitude']

class WilayaDeleteView(DeleteView):
    model = Transmission
    success_url = reverse_lazy('wilaya-change')

class WilayaUpdateView(UpdateView):
    model = Wilaya
    fields = ['code','name','ar_name','longitude','latitude']

    def test_func(self):
        Wilaya = self.get_object()
        return True


# def WilayaChange(request):
#     Wilayas = Wilaya.objects.all()
#     context = {
#         'wilayas':Wilayas,
#     }
#     return render(request, 'setup/wilaya_change.html', context)

class WilayaListView(ListView):
    model = Wilaya
    template_name = 'setup/wilaya_change.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'wilayas'
    paginate_by = 8

#######################
class CommuneCreateView(CreateView):
    model = Commune
    fields = ['post_code','name','wilaya_id','ar_name','longitude','latitude']

class CommuneDeleteView(DeleteView):
    model = Commune
    success_url = reverse_lazy('commune-change')

class CommuneUpdateView(UpdateView):
    model = Commune
    fields = ['post_code','name','wilaya_id','ar_name','longitude','latitude']

    def test_func(self):
        Commune = self.get_object()
        return True


# def CommuneChange(request):
#     Communes = Commune.objects.all()
#     context = {
#         'communes':Communes,
#     }
#     return render(request, 'setup/commune_change.html', context)

class CommuneListView(ListView):
    model = Commune
    template_name = 'setup/commune_change.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'communes'
    paginate_by = 8

#######################