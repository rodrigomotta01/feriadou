from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.db import models
from .models import Feriado, Local
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import login, logout, authenticate
import calendar
from datetime import date

# Create your views here.
def calendar_view(request, year=None, month=None):
    #CALENDARIO

    now = date.today()
    if year is None:
        year = now.year
    if month is None:
        month = now.month

    if month == 1:
        previous_month = 12
        previous_year = year - 1
    else:
        previous_month = month - 1
        previous_year = year

    if month == 12:
        next_month = 1
        next_year = year + 1
    else:
        next_month = month + 1
        next_year = year

    # Create a plain text calendar
    cal = calendar.TextCalendar(calendar.SUNDAY)
    month_calendar = cal.monthdayscalendar(year, month) # days of current month

    months_pt = {
        1: "Janeiro",
        2: "Fevereiro",
        3: "Março",
        4: "Abril",
        5: "Maio",
        6: "Junho",
        7: "Julho",
        8: "Agosto",
        9: "Setembro",
        10: "Outubro",
        11: "Novembro",
        12: "Dezembro"
    }

    # Get month name
    month_name = months_pt[month]

    #FERIADOS PROXIMOS
    today = date.today()
    current_month = today.month
    current_day = today.day
    
    # Get upcoming holidays this year
    feriados = Feriado.objects.filter(
        models.Q(month__gt=current_month) |
        models.Q(month=current_month, day__gte=current_day)
    ).order_by('month', 'day')[:5]
    
    feriados_mes = Feriado.objects.filter(month=month)
    feriados_days = {feriado.day for feriado in feriados_mes}

    context = {
        'next_month': next_month,
        'next_year': next_year,
        'previous_month': previous_month,
        'previous_year': previous_year,
        'feriados': feriados,
        'year' : year,
        'month' : month,
        'month_name': month_name,
        'month_calendar': month_calendar,
        'feriados_days': feriados_days,
    }

    return render(request, 'calendar.html', context)