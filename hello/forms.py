from django import forms
from django.contrib.auth.forms import UserCreationForm 


class Calendar(UserCreationForm):
	weekdays = ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"]
	days = []
	users = []