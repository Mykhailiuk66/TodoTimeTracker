from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .forms import CustomUserCreationForm, ProfileForm
from timeline.models import Record
# Create your views here.

def login_user(request):
    page = 'login'
    
    if request.user.is_authenticated:
        return redirect('profile')
    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        try:
            user = User.objects.get(username=username)
        except:
            print("User does not exist")
            
        user = authenticate(request, username=username, password=password)
        
        if user:
            login(request, user)
            return redirect('profile')
        else:
            print('Username or Password is incorrect')
        
    
    context = {
        'page': page
    }
    return render(request, 'users/login_register.html', context=context)


def register_user(request):
    page = 'register'
    form = CustomUserCreationForm()
    
    if request.user.is_authenticated:
        return redirect('profile')
    
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            
            login(request, user)
            return redirect('todo')
        else:
            print('error')
             
    
    context = {
        'page': page,
        'form': form,
    }
    return render(request, 'users/login_register.html', context=context)


def logout_user(request):
    logout(request)
    print('User was logout')
    
    return redirect('todo')


@login_required(login_url='login')
def profile(request):
    profile = request.user.profile
    total_tasks = profile.task_set.count()
    total_completed_tasks = profile.task_set.filter(done=True).count()
    total_in_progress_tasks = total_tasks - total_completed_tasks
    last_records = Record.objects.filter(
                                        Q(timeline__owner=profile) &
                                        Q(end_time__isnull=False)
                                        ).order_by('-end_time')[:15]
    
    try:
        max_period = max(last_records, key=lambda record: record.periodSeconds).periodSeconds
    except:
        max_period = 0
    
    context = {
        'profile': profile,
        'total_tasks': total_tasks,
        'total_completed_tasks': total_completed_tasks,
        'total_in_progress_tasks': total_in_progress_tasks,
        'last_records': last_records,
        'max_period': max_period,
        
    }
    return render(request, 'users/account.html', context=context)



@login_required(login_url='login')
def edit_profile(request):
    profile = request.user.profile
    form = ProfileForm(instance=profile)
    
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            
            return redirect('profile')
    
    context = {
        'form': form
    }
    return render(request, 'form-template.html', context=context)
    
    