from django.urls import path, re_path
from apps.labdbAPI import views

#labdb/*
urlpatterns = [

    # get meter config api
    path('meterconfig', views.getmeterConfig, name='meterConfig'),
    # register meter api
    path('register', views.registerMeter, name='registerMeter'),
    # delete meter api
    path('remove', views.removeMeter, name='removeMeter'),

]