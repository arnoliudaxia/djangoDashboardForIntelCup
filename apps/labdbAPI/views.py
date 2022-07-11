import json
import uuid

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render,HttpResponse
from apps.labdbAPI.models import *
from django.core import serializers

#labdb/meterconfig
@login_required(login_url="/login/")
def getmeterConfig(request):
    configs=meter_config.objects.all()
    meters_json={"meters":[],"labels":["表GUID","表名"]}
    for meter in configs:
        meters_json["meters"].append({
            "meterGUID":meter.meterGUID,
            "meterName":meter.meterName
        })
    print(meters_json)

    return JsonResponse(meters_json)
    # return HttpResponse(json.dumps(meters_json))

#labdb/register
@login_required(login_url="/login/")
def registerMeter(request):
    metername = request.GET.get("name")
    if metername:
        meter_config.objects.create(meterName=metername,meterGUID=str(uuid.uuid1()))
        return HttpResponse("注册表成功")
    else:
        return HttpResponse("没有写表名！")

#labdb/remove
@login_required(login_url="/login/")
def removeMeter(request):
    guid = request.GET.get("guid")
    if guid:
        if meter_config.objects.all().filter(meterGUID=guid).count()==1:
            meter_config.objects.all().get(meterGUID=guid).delete()
        else:
            return HttpResponse("没有找到这个表！")
        return HttpResponse("200")
    else:
        return HttpResponse("没有写表GUID！")

