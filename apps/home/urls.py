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
    # 每一个lab内页，应该包含该lab下meter的管理和数据可视化
    # 这里用path匹配而不是str的原因是没法匹配中文
    path('lab/<path:labname>', views.labview, name='lab'),
    # AI进程管理页面
    path('AI', views.aiview, name='aiview'),
    # kill ai process
    path('killai/<int:pid>', views.killai, name='killai'),
    # create ai process
    path('createai', views.createai, name='creatai'),

    re_path("UIExamples/.*", views.debugPages, name='debugPages'),
    # Matches any html file
    re_path(r'^.*\.*', views.pages, name='pages'),

]
