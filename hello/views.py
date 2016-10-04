from django.shortcuts import render
from django.http import HttpResponse

from datetime import datetime, timedelta

from .forms import Calendar
from .models import UserSkif
from .models import StorableDate

from django.conf import settings

import json

# Create your views here.
def index(request):
    form = Calendar()

    stored_date = list(StorableDate.objects.all())[0]
    date = datetime(year=stored_date.year, 
                    month=stored_date.month, 
                    day=stored_date.day)

    form.days = []
    for i in range(settings.DAYS_ON_PAGE):
        form.days.append({'day_of_week': form.weekdays[date.weekday()], 'day_of_month': date.day })
        date = date + timedelta(days=1)

    form.users = list(UserSkif.objects.all())
    form.users.sort(key = user_name)


    if request.method == "POST":
        x = int(request.POST.get('x'))
        y = int(request.POST.get('y'))

        response_data = {}
        if x >= settings.MIN_X and y >= settings.MIN_Y:
            user = form.users[y-2]
            choises = user.get_choises()
            choises[x-1] = (choises[x-1] + 1) % settings.STATES_COUNT
            user.set_choises(choises)
            user.save()
            form.users = UserSkif.objects.all()
    
            response_data = {'MIN_X':settings.MIN_X, 
                            'MIN_Y':settings.MIN_Y, 
                            'STATE': settings.STATES[choises[x-1]],
                            'STATES_COUNT': settings.STATES_COUNT,
                            }

        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json"
        )

    for user in form.users:
        choises = user.get_choises()
        states = [settings.STATES[choise] for choise in choises]
        user.set_choises(states)

    return render(request, 
                  'index.html', 
                  { 'form': form, 
                  })

def last(request):
    form = Calendar()

    stored_date = list(StorableDate.objects.all())[0]
    last_date = datetime(year=stored_date.year, 
                    month=stored_date.month, 
                    day=stored_date.day)

    first_date = last_date - settings.PERIOD_TO_STORAGE_WORKS
    
    form.dates = get_dates_list(first_date, last_date, timedelta(days=1))
    form.users = list(UserSkif.objects.all())
    form.users.sort(key = user_name)

    for user in form.users:
        user.last_work_guide_mark = []
        for date in form.dates:
            his_last_works = user.get_last_works()
            if date in his_last_works:
                user.last_work_guide_mark.append(settings.WORK_STATE_NUM)
            else:
                user.last_work_guide_mark.append(0)
        user.last_work_guide_mark = [settings.STATES[guide_mark] for guide_mark in user.last_work_guide_mark]

    return render(request, 
                  'last.html', 
                  { 'form': form,
                  })

def new_day(request):
    generate_new_day()
    return index(request)

def generate_new_day():
    users = list(UserSkif.objects.all())

    stored_date = list(StorableDate.objects.all())[0]
    today = datetime(year=stored_date.year, 
                     month=stored_date.month, 
                     day=stored_date.day)

    users.sort(key = last_works_count)
    wants =          [user for user in users if settings.STATES[user.get_choises()[settings.DAYS_WITH_SHEDULE]] == "want"]
    indifferentlys = [user for user in users if settings.STATES[user.get_choises()[settings.DAYS_WITH_SHEDULE]] == "indifferently"]
    sorted_users = wants + indifferentlys

    for user in sorted_users[:2]:
        choises = user.get_choises()
        choises[settings.DAYS_WITH_SHEDULE] = settings.WORK_STATE_NUM
        user.set_choises(choises)
        user.save()

    for user in users:
        last_works = user.get_last_works()
        if user.get_choises()[0] == settings.WORK_STATE_NUM:
            last_works.append(today)

        handled_works = drop_very_last_works(last_works, today - settings.PERIOD_TO_STORAGE_WORKS)
        user.set_last_works(handled_works)

        choises = user.get_choises()
        user.set_choises(shift(choises))
        user.save()

    today = today + timedelta(days=1)
    stored_date.year = today.year
    stored_date.month = today.month
    stored_date.day = today.day
    stored_date.save()


def get_dates_list(first_date, last_date, timedelta):
    result = []
    current = first_date

    while current <= last_date:
        result.append(current)
        current += timedelta
    return result

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

def user_name(user):
    return user.name