from multiprocessing import context
from django.shortcuts import render, redirect
from accounts.models import User
from django.db.models import Q
import agency
from .forms import AdminForm, AgencyForm, AgencyFormCreate, UserForm
# Create your views here.
def dashboard(request):
    return render(request, 'a/dashboard.html')
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
def manage_users_search(request):
    if request.method == 'GET':
        q=request.GET.get('search', ' ')
        result = User.objects.filter(Q(username__icontains=q))
        context={'result':result}
    
    return render(request, 'a/users/search.html', context)
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

# setup
def setup(request):
    return render(request, 'a/setup.html')

