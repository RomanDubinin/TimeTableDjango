from django.shortcuts import render
from django.http import HttpResponse

from datetime import datetime, timedelta

from .forms import Calendar
from .models import UserSkif

from django.conf import settings

# Create your views here.
def index(request):
    # return HttpResponse('Hello from Python!')
    form = Calendar()
    current_wd = 3
    current_md = 14

    date = datetime(year=2016, month=3, day=17)

    form.days = []
    for i in range(settings.DAYS_ON_PAGE):
    	form.days.append({'day_of_week': form.weekdays[date.weekday()], 'day_of_month': date.day })
    	date = date + timedelta(days=1)

    form.users = UserSkif.objects.all()
    
    return render(request, 'index.html', {'form': form})

def create_post(request):
    if request.method == 'POST':
        post_text = request.POST.get('the_post')
        response_data = {}
        print("------------------------------------------------------------------")
        print(post_text)
        
        print("------------------------------------------------------------------")
        

        return index(request)
    else:
        return index(request)