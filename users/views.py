from django.contrib.auth import login as auth_login
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, reverse,get_object_or_404,redirect
from .forms import RegisterForm, UserUpdateForm, ProfileUpdateForm, CustomRegisterForm
from django. contrib import messages
from django.contrib.auth.decorators import login_required
from account.models import Coordinator, Dean, Hod, Supervisor, StudentGroup, FinalProjects
from users.models import CustomerUser


def home(request):
    mapbox_access_token = 'pk.eyJ1IjoiMjE3MDA0NjQ0IiwiYSI6ImNrYTg2dTRhcTBhOXoydG1rdmRudWwyd3cifQ.WSQ6Oy9NcqmxiXkNYJ3UkQ'
    project = FinalProjects.objects.all()
    context = {
        'mapbox_access_token':mapbox_access_token,
        'project': project
    }
    return render(request, 'home.html', context=context)


def userRegisterpage(request):
    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            # auth_login(request, user)
            messages.success(request, 'Account created!')
            return HttpResponseRedirect(reverse('register_user'))

    else:
        form = RegisterForm()
    return render(request, 'users/register.html', {'form':form})


@login_required
def customRegisterpage(request):
    if request.method == 'POST':
        form = CustomRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            # auth_login(request, user)
            messages.success(request, 'Account created!')
            return HttpResponseRedirect(reverse('home'))

    else:
        form = CustomRegisterForm()
    return render(request, 'users/custom_register.html', {'form':form})


@login_required
def profile(request):
    if request.method == 'POST':
        p_form = ProfileUpdateForm(request.POST,request.FILES,instance=request.user.profile)

        if p_form.is_valid():
            p_form.save()
            messages.success(request, ' your account has been Updated!')
            return redirect('home')

    else:
        p_form = ProfileUpdateForm()

    context = {
        'p_form': p_form
    }

    return render(request,'users/profile.html',context)


@login_required
def account(request):
    if request.method == 'POST':
        form = UserUpdateForm(request.POST,instance=request.user)

        if form.is_valid():
            form.save()
            messages.success(request, ' your account has been Updated!')
            return redirect('login')

    else:
        form = UserUpdateForm(instance=request.user)

    context = {
        'form': form,
    }

    return render(request,'users/account.html', context)


@login_required
def dashboard(request, pk):
    users = User.objects.get(pk=pk)
    hods = Hod.objects.filter(hod_name=users)
    custom = CustomerUser.objects.filter(username=users)
    students = StudentGroup.objects.filter(student_name=users)
    deans = Dean.objects.filter(dean_name=users)
    coordinators = Coordinator.objects.filter(user_name=users)
    teachers = Supervisor.objects.filter(supervisor_name=users)

    context = {
        'users': users,
        'students': students,
        'custom': custom,
        'deans': deans,
        'hods': hods,
        'teachers': teachers,
        'coordinators': coordinators,
    }
    return render(request, 'users/dashboard.html', context=context)