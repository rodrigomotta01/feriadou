from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views


urlpatterns = [
    path('', views.calendar_view, name='calendarcurrent_view'),
    path('calendar/<int:year>/<int:month>/', views.calendar_view, name='calendar_view'),
]