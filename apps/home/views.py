# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
import os
import subprocess

from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.shortcuts import render, redirect
from core.settings import DEBUG

from apps.labdbAPI.models import lab_config, meter_config, ai_process
import psutil

isDebug = True


def getAllLabNames():
    '''
    获取所有实验室名称

    :return: 返回一个list，包含所有实验室名称
    '''

    labs = lab_config.objects.all()
    result = []
    for lab in labs:
        result.append(lab.labName)
    return result


def getAllMetersUnderLab(labname: str):
    '''
    获取某个实验室下的所有表

    :param labname: 实验室名称
    :return: 返回一个列表，包含所有表的GUID和名字的键值对
    '''

    meters = meter_config.objects.all().filter(belongLab=labname)
    result = []
    for meter in meters:
        result.append({"GUID": meter.meterGUID, "name": meter.meterName})
    return result


def getAllAiProcess():
    '''
    获取正在运行的所有AI进程（通过数据库）

    :return:
    '''
    # 这里不用本地的进程管理是为了让web app于ai解耦
    # 必须假设Web App是不可靠的，不能web挂掉后就没法管理AI进程了
    # 因此，AI进程启动后要主动向数据库记录自己的pid
    aiProcesses = ai_process.objects.all()
    result = []
    for process in aiProcesses:
        result.append({"pid": process.pid,
                       "takeinVideo": process.takeinVideo,
                       "belong2Meter": process.belong2Meter})
    return result


# 首页重定向到welcome.html
@login_required(login_url="/login/")
def index(request):
    return redirect("/welcome.html")


@login_required(login_url="/login/")
def homepage(request):
    context = {
        "debug": isDebug,
        "url": request.path,
        "labNames": getAllLabNames()
    }

    return render(request, "home/welcome.html", context)


@login_required(login_url="/login/")
def labview(request, labname: str):
    # 在每个实验室内的调用数据库API需要把url重定向到根目录
    if "labdb" in labname:
        # 在有GET参数的时候要一并重定向过去
        labname += "?" + request.GET.urlencode()
        print(f"redirect to {'/' + labname}")
        return redirect("/" + labname)
    # 获取实验室下的所有meter，一个meter制作一个表格
    context = {
        "debug": isDebug,
        "url": request.path,
        "labNames": getAllLabNames(),
        "currentLabName": labname,
        "metersInLab": getAllMetersUnderLab(labname)
    }
    return render(request, "home/lab.html", context)


@login_required(login_url="/login/")
def aiview(request):
    context = {
        "debug": isDebug,
        "url": request.path,
        "aiprocess": getAllAiProcess(),
        "labNames": getAllLabNames(),
    }
    return render(request, "home/AI.html", context)


# killai/<int:pid>?redir=
@login_required(login_url="/login/")
def killai(request, pid: int):
    if psutil.pid_exists(pid):
        p = psutil.Process(pid)
        if p.status() == "running":
            p.terminate()
    ai_process.objects.all().get(pid=pid).delete()
    return redirect(request.GET.get("redir"))


from core.settings import AI_CMD, AI_PWD


# createai?url=&meter=&redir=
@login_required(login_url="/login/")
def createai(request):
    url = request.GET.get("url")
    if url.startswith("file"):
        url = url[7:]
    meter = request.GET.get("meter")
    if url and meter:
        print('创建本地ai进程')
        print(AI_CMD+" "+url+" "+meter)
        subp = subprocess.Popen(AI_CMD+" "+url+" "+meter, cwd=AI_PWD, shell=True, executable='/bin/bash')
    return redirect(request.GET.get("redir"))


@login_required(login_url="/login/")
def debugPages(request):
    print("看看Example吧")
    if not isDebug:
        return render(request, 'home/page-404.html')
    sub_page = request.path.split('/')[-1]
    html_template = loader.get_template('home/UIExamples/' + sub_page)
    return HttpResponse(html_template.render({"debug": isDebug}, request))


@login_required(login_url="/login/")
def pages(request):
    context = {"debug": True}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        sub_page = request.path.split('/')[-1]

        if sub_page == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))
        context['segment'] = sub_page

        html_template = loader.get_template('home/' + sub_page)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))
