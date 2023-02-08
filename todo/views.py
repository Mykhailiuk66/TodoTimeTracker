from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
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

    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            profile = request.user.profile

            task = form.save(commit=False)
            task.owner = profile
            task.save()
            form.save_m2m()

            messages.success(request, 'Task was added successfuly!')
            return redirect('todo')
    elif request.method == 'GET':
        form = TaskForm()

    context = {'form': form}
    return render(request, 'form-template.html', context=context)


@login_required(login_url='login')
def update_task(request, pk):
    profile = request.user.profile
    task = profile.task_set.get(id=pk)

    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()

            messages.success(request, 'Task was updated successfuly!')
            return redirect('todo')
    elif request.method == 'GET':
        form = TaskForm(instance=task)

    context = {
        'form': form
    }
    return render(request, 'form-template.html', context=context)


@login_required(login_url='login')
@csrf_exempt
def task_done(request, pk):

    if request.method == 'POST':
        profile = request.user.profile
        task = profile.task_set.get(id=pk)
        task.done = not task.done
        task.save()

        if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
            return JsonResponse({'checked': task.done}, safe=False)
        else:
            return redirect('todo')
    

    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        return JsonResponse({'Error': 'Only POST method is allowed'}, safe=False)
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

    if request.method == 'POST':
        form = TagForm(request.POST)
        if form.is_valid():
            form.save()

            messages.success(request, 'Tag was added successfuly!')
            return redirect('profile')
        else:
            messages.warning(request, 'Tag with this name already exists.')
    elif request.method == 'GET':
        form = TagForm()

    context = {'form': form}
    return render(request, 'form-template.html', context=context)


@login_required(login_url='login')
def update_tag(request):
    if not request.user.is_superuser:
        return redirect('profile')

    if request.method == 'POST':
        form = UpdateTagForm(request.POST)
        if form.is_valid():
            tag = Tag.objects.filter(name=request.POST['tag_name']).first()
            if not tag:
                messages.warning(request, 'Tag does not exist')
                return redirect('update-tag')

            new_tag = Tag.objects.filter(
                name=request.POST['new_tag_name']).first()
            if new_tag:
                messages.warning(request, 'Tag with this name already exists')
                return redirect('update-tag')

            tag.name = request.POST['new_tag_name']
            tag.save()

            messages.success(request, 'Tag was updated successfuly!')
            return redirect('profile')
    elif request.method == 'GET':
        form = UpdateTagForm()

    context = {'form': form}
    return render(request, 'form-template.html', context=context)


@login_required(login_url='login')
def delete_tag(request):
    if not request.user.is_superuser:
        return redirect('profile')

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
    elif request.method == 'GET':
        form = DeleteTagForm()

    context = {'form': form}
    return render(request, 'form-template.html', context=context)
