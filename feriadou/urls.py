from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views


urlpatterns = [
    path('', views.calendar_view, name='calendarcurrent_view'),
    path('calendario/<int:year>/<int:month>/', views.calendar_view, name='calendar_view'),
    path('cadastro/', views.my_signup_view.as_view(), name='signup_view'),
    path('login/', views.my_login_view.as_view(), name='login_view'),
    path('logout/', views.my_logout_view.as_view(), name='logout_view'),
    path('passwordreset/', views.my_passwordreset_view.as_view(), name='passwordreset_view')
]