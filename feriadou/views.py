from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.db import models
from .models import Feriado
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import login, logout, authenticate
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView
from .forms import LoginForm, SignUpForm, UsernamePasswordResetForm, PasswordResetForm
from google.oauth2 import id_token
from google.auth.transport import requests
from django.conf import settings
from django.contrib import messages
import logging
import calendar
from datetime import date
from django.urls import reverse_lazy

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
        models.Q(month=current_month, day__gte=current_day-1)
    ).order_by('month', 'day')[:5]
    
    feriados_mes = Feriado.objects.filter(month=month)
    feriados_days = {feriado.day for feriado in feriados_mes}

    feriados_municipais = {f.day for f in Feriado.objects.filter(escopo="Municipal", month=month)}
    feriados_estaduais = {f.day for f in Feriado.objects.filter(escopo="Estadual", month=month)}
    feriados_nacionais = {f.day for f in Feriado.objects.filter(escopo="Nacional", month=month)}

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
        'feriadosnacionais': feriados_nacionais
        
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
    success_url = reverse_lazy("password_reset_done")
    email_template_name = 'registration/password_reset_email.html'
    subject_template_name = 'registration/password_reset_subject.txt'

"""@csrf_exempt
def login_google_view(request):
    if request.method == 'POST':

        token = request.POST.get("credential")

        try:
            data = id_token.verify_oauth2_token(
                token,
                requests.Request(),
                settings.GOOGLE_OAUTH_CLIENT_ID,
                clock_skew_in_seconds=300  # tolera até 5 minutos de diferença
            )
            
            email = data["email"]
            name = data.get("name", "")

            user, created = Usuario.objects.get_or_create(
                username=email,
                defaults={
                    "first_name": name.split()[0] if name else "",
                    "last_name": " ".join(name.split()[1:]) if name and len(name.split()) > 1 else "",
                    "email": email,
                }
            )

            # Se o usuário já existia mas não tinha o email preenchido, atualiza e salva
            if not created and (not user.email or user.email != email):
                user.email = email
                user.save()

            login(request, user)
            return redirect("home_view")
            
        except ValueError:
            logging.exception("Erro ao verificar token Google")
            return HttpResponse(status=403)"""