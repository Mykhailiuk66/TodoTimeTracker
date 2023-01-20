from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import messages
from django.utils import timezone
from django.db.models import Q
from .models import Timeline, Record
from .forms import TimelineForm


@login_required(login_url='login')
def timelines(request):
    profile = request.user.profile
    timelines = profile.timeline_set.all()
    last_records = Record.objects.filter(
        Q(timeline__owner=profile) &
        Q(end_time__isnull=False)
    ).order_by('-end_time')[:10]
    active_records = Record.objects.filter(
        Q(timeline__active=True) &
        Q(end_time__isnull=True)
    ).distinct().order_by('-start_time')

    context = {
        'timelines': timelines,
        'last_records': last_records,
        'active_records': active_records,
    }
    return render(request, 'timeline/timeline.html', context=context)


@login_required(login_url='login')
def create_timeline(request):

    if request.method == 'POST':
        form = TimelineForm(request.POST)
        if form.is_valid():
            profile = request.user.profile
            timeline = form.save(commit=False)
            timeline.owner = profile
            timeline.save()
            messages.success(request, 'Timeline was added successfuly!')

            return redirect('timeline')
    elif request.method == 'GET':
        form = TimelineForm()

    context = {
        'form': form
    }
    return render(request, 'form-template.html', context)


@login_required(login_url='login')
def update_timeline(request, pk):
    profile = request.user.profile
    timeline = profile.timeline_set.get(id=pk)

    if request.method == 'POST':
        form = TimelineForm(request.POST, instance=timeline)
        if form.is_valid():
            form.save()

            messages.success(request, 'Timeline was updated successfuly!')
            return redirect('timeline')
    elif request.method == 'GET':
        form = TimelineForm(instance=timeline)

    context = {'form': form}
    return render(request, 'form-template.html', context)


@login_required(login_url='login')
def delete_timeline(request, pk):
    profile = request.user.profile
    timeline = profile.timeline_set.get(id=pk)
    timeline.delete()

    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        return JsonResponse('Deleted', safe=False)
    else:
        return redirect('timeline')


@login_required(login_url='login')
def start_timeline(request, pk):
    profile = request.user.profile
    timeline = profile.timeline_set.get(id=pk)

    record = Record.objects.create(
        timeline=timeline,
    )

    timeline.active = True
    timeline.save()

    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        return JsonResponse(f'Timeline "{timeline.title}" started', safe=False)
    else:
        return redirect('timeline')


@login_required(login_url='login')
def stop_timeline(request, pk):
    profile = request.user.profile
    timeline = profile.timeline_set.get(id=pk)
    record = timeline.record_set.last()

    if record and not record.end_time:
        record.end_time = timezone.now()
        record.save()

    timeline.active = False
    timeline.save()

    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        return JsonResponse(f'Timeline "{timeline.title}" stopped', safe=False)
    else:
        return redirect('timeline')
