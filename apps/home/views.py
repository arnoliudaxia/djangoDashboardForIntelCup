# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.shortcuts import render,redirect

isDebug = True


@login_required(login_url="/login/")
def index(request):
    return redirect("home/welcome.html")

@login_required(login_url="/login/")
def debugPages(request):
    print("看看Example吧")
    if not isDebug:
        return render(request,'home/page-404.html')
    sub_page = request.path.split('/')[-1]
    html_template = loader.get_template('home/UIExamples/' + sub_page)
    return HttpResponse(html_template.render({"debug":isDebug}, request))

@login_required(login_url="/login/")
def pages(request):
    context = {"debug": isDebug}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        sub_page = request.path.split('/')[-1]

        if sub_page == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))
        context['segment'] = sub_page

        if ("lab" in sub_page) and request.GET.get("id"):
            context["labname"] = request.GET.get("id")

        html_template = loader.get_template('home/' + sub_page)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))
