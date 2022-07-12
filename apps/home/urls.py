# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from apps.home import views

urlpatterns = [

    # index redir
    path('', views.index, name='index'),
    # The home page
    path('welcome.html', views.homepage, name='welcome'),




    re_path("UIExamples/.*", views.debugPages, name='debugPages'),
    # Matches any html file
    re_path(r'^.*\.*', views.pages, name='pages'),

]
