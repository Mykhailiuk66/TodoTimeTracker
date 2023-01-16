from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import messages
from .forms import TaskForm, TagForm, UpdateTagForm, DeleteTagForm
from .models import Task, Tag
from .utils import pagination_tasks


@login_required(login_url='login')
def tasks(request):
    profile = request.user.profile
    tasks = profile.task_set.all()
    custom_range, tasks = pagination_tasks(request, tasks, 7)
    
    
    context = {
        'tasks': tasks,
        'custom_range': custom_range,
    }
    return render(request, 'todo/todo.html', context=context)


@login_required(login_url='login')
def create_task(request):
    form = TaskForm()
    
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            profile = request.user.profile
            
            task = form.save(commit=False)
            task.owner = profile
            task.save()
            
            messages.success(request, 'Task was added successfuly!')
            return redirect('todo')
    
    context = {'form': form}
    return render(request, 'form-template.html', context=context)


@login_required(login_url='login')
def update_task(request, pk):
    profile = request.user.profile
    task = profile.task_set.get(id=pk)
     
    form = TaskForm(instance=task)

    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            
            messages.success(request, 'Task was updated successfuly!')
            return redirect('todo')
    
    context = {
        'form': form
    }
    return render(request, 'form-template.html', context=context)


@login_required(login_url='login')
def task_done(request, pk):
    profile = request.user.profile
    task = profile.task_set.get(id=pk)
    task.done = not task.done
    task.save()
    
    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        return JsonResponse({'checked': task.done}, safe=False)
    else:
        return redirect('todo')


@login_required(login_url='login')
def delete_task(request, pk):
    profile = request.user.profile
    task = profile.task_set.get(id=pk)
    task.delete()
    
    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        return JsonResponse('deleted', safe=False)
    else:
        return redirect('todo')


@login_required(login_url='login')
def tags(request):
    tags = Tag.objects.all()
    
    context = {'tags': tags}
    return render(request)   
    
    
    
@login_required(login_url='login')
def create_tag(request):
    if not request.user.is_superuser:
        return redirect('profile')
    
    form = TagForm()
    if request.method == 'POST':
        form = TagForm(request.POST)
        if form.is_valid():
            form.save()
            
            messages.success(request, 'Tag was added successfuly!')         
            return redirect('profile')
        else:
            messages.warning(request, 'Tag with this name already exists.')         
            
    
    context = {'form': form}
    return render(request, 'form-template.html', context=context)
    
    
@login_required(login_url='login')
def update_tag(request):
    if not request.user.is_superuser:
        return redirect('profile')

    form = UpdateTagForm()
    if request.method == 'POST':
        form = UpdateTagForm(request.POST)
        if form.is_valid():
            tag = Tag.objects.filter(name=request.POST['tag_name']).first()
            if not tag:
                messages.warning(request, 'Tag does not exist')         
                return redirect('update-tag')

            new_tag = Tag.objects.filter(name=request.POST['new_tag_name']).first()
            if new_tag:
                messages.warning(request, 'Tag with this name already exists')         
                return redirect('update-tag')
            
            tag.name = request.POST['new_tag_name']
            tag.save()
                    
            messages.success(request, 'Tag was updated successfuly!')         
            return redirect('profile')
            
    context = {'form': form}
    return render(request, 'form-template.html', context=context)
    
    
@login_required(login_url='login')
def delete_tag(request):
    if not request.user.is_superuser:
        return redirect('profile')

    form = DeleteTagForm()
    if request.method == 'POST':
        form = DeleteTagForm(request.POST)
        if form.is_valid():
            tag = Tag.objects.filter(name=request.POST['tag_name']).first()
            
            if tag:
                tag.delete()
            else:
                messages.warning(request, 'Tag does not exist')         
                return redirect('delete-tag')
                    
            messages.success(request, 'Tag was deleted successfuly!')         
            return redirect('profile')
            
            
    context = {'form': form}
    return render(request, 'form-template.html', context=context)
