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
    # record meter data api
    path('record', views.record, name='record'),
    # get meter data api
    path('retrive', views.getMeterData, name='getMeterData'),
    # get labs config api
    path('labsconfig', views.getlabsConfig, name='getlabsConfig'),
    # register lab api
    path('registerLab', views.registerLab, name='registerLab'),
    # delete lab api
    path('removeLab', views.removeLab, name='removeLab'),
    # get camera img api
    path('preview/<int:pid>', views.preview, name='preview'),
    # export meter data api
    path('export/<str:guid>', views.export, name='export'),
]