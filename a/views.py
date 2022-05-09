from django.shortcuts import render, redirect
from accounts.models import User
from .forms import AgencyForm, UserForm
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