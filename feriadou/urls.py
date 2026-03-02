from django.urls import path
from django.urls import include, path
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.calendar_view, name='calendarcurrent_view'),
    path('calendario/<int:year>/<int:month>/', views.calendar_view, name='calendar_view'),
    path('cadastro/', views.my_signup_view.as_view(), name='signup_view'),
    path('login/', views.my_login_view.as_view(), name='login_view'),
    path('logout/', views.my_logout_view.as_view(), name='logout_view'),
    path('passwordreset/', views.my_passwordreset_view.as_view(), name='passwordreset_view'),
    path('passwordreset/done/', views.my_passwordresetdone_view.as_view(), name='passwordresetdone_view'),
    path('passwordreset/confirm/<uidb64>/<token>/', views.my_passwordresetconfirm_view.as_view(), name='passwordresetconfirm_view'),
    path('passwordreset/complete/', views.my_passwordresetcomplete_view.as_view(), name='passwordresetcomplete_view'),
    path('solicitacaoferiado/', views.feriadorequest_view.as_view(), name='feriadorequest_view')
]
