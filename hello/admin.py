from django.contrib import admin

# Register your models here.

from .models import UserSkif
from .models import StorableDate

admin.site.register(UserSkif)
admin.site.register(StorableDate)