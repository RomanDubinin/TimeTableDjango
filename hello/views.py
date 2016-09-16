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

def numbers_to_stetes(arr, states):
    res = []
    for i in range(len(arr)):
        res.append(states[arr[i]])
    return res