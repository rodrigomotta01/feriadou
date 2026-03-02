from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import models
from .models import Feriado
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import login
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from .forms import LoginForm, SignUpForm, PasswordResetForm, FeriadoRequestForm
from django.contrib import messages
import calendar
from datetime import date
from django.urls import reverse_lazy
import requests
from django.core.cache import cache

def get_municipios(uf):
    cache_key = f'municipios_{uf}'
    municipios = cache.get(cache_key)
    if municipios:
        return municipios
    
    link = f"https://servicodados.ibge.gov.br/api/v1/localidades/estados/{uf}/municipios"
    requisicao = requests.get(link, timeout=3)
    info = requisicao.json()
    
    municipios = []

    for municipio in info:
        municipios.append(municipio['nome'])

    cache.set(cache_key, municipios, timeout=60*60*2)
    return municipios

def calendar_view(request, year=None, month=None):
    
    uf = request.GET.get('uf')
    municipio = request.GET.get('municipio')

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
        models.Q(month=current_month, day__gte=current_day-1)
    ).order_by('month', 'day')[:5]
    
    feriados_mes = Feriado.objects.filter(month=month)
    feriados_days = {feriado.day for feriado in feriados_mes}

    feriados_municipais = {f.day for f in Feriado.objects.filter(escopo="Municipal", month=month, estado=uf, municipio=municipio)}
    feriados_estaduais = {f.day for f in Feriado.objects.filter(escopo="Estadual", month=month, estado=uf)}
    feriados_nacionais = {f.day for f in Feriado.objects.filter(escopo="Nacional", month=month)}

    if uf:
        municipios = get_municipios(uf)
    else:
        municipios = None

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
        'feriadosmunicipais': feriados_municipais,
        'feriadosestaduais': feriados_estaduais,
        'feriadosnacionais': feriados_nacionais,
        'uf': uf,
        'municipio' : municipio,
        'municipios' : municipios
        
    }

    return render(request, 'calendar.html', context)

class my_signup_view(CreateView):
    form_class = SignUpForm
    template_name = 'signup.html'
    success_url = reverse_lazy('calendarcurrent_view')

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        return response

class my_login_view(LoginView):
    template_name = 'login.html'
    authentication_form = LoginForm
    next_page = 'calendarcurrent_view'
    
    def form_valid(self, form):
        messages.success(self.request, "Bem vindo ao Feriadou!")
        return super().form_valid(form)
    
class my_logout_view(LogoutView):
    next_page = 'calendarcurrent_view'

class my_passwordreset_view(PasswordResetView):
    template_name = 'passwordreset.html'
    form_class = PasswordResetForm
    success_url = reverse_lazy("passwordresetdone_view")
    email_template_name = 'registration/password_reset_email.html'
    html_email_template_name = 'registration/password_reset_email.html'
    subject_template_name = 'registration/password_reset_subject.txt'

class my_passwordresetdone_view(PasswordResetDoneView):
    template_name = 'passwordresetdone.html'

class my_passwordresetconfirm_view(PasswordResetConfirmView):
    template_name = 'passwordresetconfirm.html'
    success_url = reverse_lazy('passwordresetcomplete_view')

class my_passwordresetcomplete_view(PasswordResetCompleteView):
    template_name = 'passwordresetcomplete.html'

class feriadorequest_view(CreateView):
    form_class = FeriadoRequestForm
    template_name = 'feriadorequest.html'
    success_url = reverse_lazy('calendarcurrent_view')
    success_url = reverse_lazy("passwordresetcomplete_view")

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        return super().form_valid(form)