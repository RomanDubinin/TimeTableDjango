from django.shortcuts import render
from django.http import HttpResponse

from datetime import datetime, timedelta

from .forms import Calendar
from .models import UserSkif

from django.conf import settings

import json

# Create your views here.
def index(request):
    form = Calendar()

    date = datetime(year=2016, month=3, day=17)

    form.days = []
    for i in range(settings.DAYS_ON_PAGE):
        form.days.append({'day_of_week': form.weekdays[date.weekday()], 'day_of_month': date.day })
        date = date + timedelta(days=1)

    form.users = UserSkif.objects.all()

    if request.method == "POST":
        x = int(request.POST.get('x'))
        y = int(request.POST.get('y'))

        response_data = {}
        if x >= settings.MIN_X and y >= settings.MIN_Y:
            user = form.users[y-2]
            days = user.getdays()
            days[x-1] = (days[x-1] + 1) % settings.STATES_COUNT
            user.setdays(days)
            user.save()
            form.users = UserSkif.objects.all()
    
            response_data = {'MIN_X':settings.MIN_X, 
                            'MIN_Y':settings.MIN_Y, 
                            'STATE': settings.STATES[days[x-1]],
                            'STATES_COUNT': settings.STATES_COUNT,
                            }

        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json"
        )

    for user in form.users:
        states = numbers_to_stetes(user.getdays(), settings.STATES)
        user.setdays(states)

    return render(request, 
                  'index.html', 
                  { 'form': form, 
                    'MIN_X':settings.MIN_X, 
                    'MIN_Y':settings.MIN_Y,
                    'STATE': "1",
                    'STATES_COUNT': settings.STATES_COUNT,
                  })

def new_day(request):
    users = list(UserSkif.objects.all())
    today = datetime.now()

    users.sort(key = last_works_count)
    wants =          [user for user in users if settings.STATES[user.getdays()[settings.DAYS_WITH_SHEDULE]] == "want"]
    indifferentlys = [user for user in users if settings.STATES[user.getdays()[settings.DAYS_WITH_SHEDULE]] == "indifferently"]
    sorted_users = wants + indifferentlys

    for user in sorted_users[:2]:
        days = user.getdays()
        days[settings.DAYS_WITH_SHEDULE] = settings.WORK_STATE
        user.setdays(days)
        user.save()

    for user in users:
        last_works = user.get_last_works()
        if user.getdays()[0] == settings.WORK_STATE:
            last_works.append(today)

        handled_works = drop_very_last_works(last_works, today - settings.PERIOD_TO_STORAGE_WORKS)
        user.set_last_works(handled_works)

        days = user.getdays()
        user.setdays(shift(days))
        user.save()
        
    return index(request)




def numbers_to_stetes(arr, states):
    res = []
    for i in range(len(arr)):
        res.append(states[arr[i]])
    return res

def drop_very_last_works(works, treshold):
    handled_works = []

    for work_date in works:
        if work_date >= treshold:
            handled_works.append(work_date)
    return handled_works

def shift(arr):
    del arr[0]
    arr.append(0)
    return arr

def last_works_count(user):
    return len(user.get_last_works())