from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404
from common.models import Event, New, Call
from django.urls import reverse
from common import models
from django.http import HttpResponse
from django.core.paginator import Paginator
from datetime import datetime, date, time, timedelta
from django.db.models import Q

def home(request):
    now = datetime.today()
    event = Event.objects.filter(date__gte =now).order_by('date')[:3]
    new = New.objects.all()[::-1][:3]
    context = {'events': event, 'news': new}
    return render(request, 'web/home.html', context)


def history(request):
    return render(request, 'web/history.html', locals())


def organizationchart(request):
    return render(request, 'web/organizationchart.html', locals())


def missionvision(request):
    return render(request, 'web/mission-vision.html', locals())


def directorymentors(request):
    return render(request, 'web/directory-mentors.html', locals())

def ventures(request):
    return render(request, 'web/ventures.html', locals())

def calls(request):
    now = datetime.today()
    call = Call.objects.select_related('entity').filter(due_date__gte =now).order_by('due_date')
    paginator = Paginator(call,3)
    page = request.GET.get('page')
    call = paginator.get_page(page)
    queryset = request.GET.get("search-call")
    if queryset:
        call = Call.objects.filter(
            Q(name__icontains = queryset),
            due_date__gte =now
        ).distinct()
    return render(request, 'web/calls.html', {'calls':call})

def news(request):
    new = New.objects.all()[::-1]
    paginator = Paginator(new,6)
    page = request.GET.get('page')
    new = paginator.get_page(page)
    queryset = request.GET.get("search-new")
    if queryset:
        new = New.objects.filter(
            Q(title__icontains = queryset) |
            Q(description = queryset)
        ).distinct()
    return render(request, 'web/news.html', {'news':new})


def events(request):
    now = datetime.today()
    event = Event.objects.filter(date__gte =now).order_by('date')
    paginator = Paginator(event,5)
    page = request.GET.get('page')
    event = paginator.get_page(page)
    queryset = request.GET.get("search-event")
    if queryset:
        event = Event.objects.filter(
            Q(title__icontains = queryset) |
            Q(description = queryset),
            date__gte =now
        ).distinct()
    return render(request, 'web/events.html', {'events':event})


def contact(request):
    return render(request, 'web/contact.html', locals())

# Event detail
def event_detail(request, event_id):
    events = Event.objects.all().order_by('-date')[:3]
    event = get_object_or_404(models.Event, id=event_id)
    context = {'sb_events': events, 'event': event}
    return render(request, 'web/event-detail.html', context)

# New detail
def new_detail(request, new_id):
    news = New.objects.all()[::-1][:3]
    new = get_object_or_404(models.New, id=new_id)
    context = {'sb_news': news, 'new': new}
    return render(request, 'web/new-detail.html', context)

def call_detail(request, call_id):
    call = get_object_or_404(models.Call, id=call_id)
    context = {'call': call}
    return render(request, 'web/call-detail.html', context)