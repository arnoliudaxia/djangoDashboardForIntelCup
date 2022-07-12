import datetime
import json
import uuid

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render,HttpResponse
from django.utils import timezone

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

#labdb/record?guid=&value=
@login_required(login_url="/login/")
def record(request):
    guid=request.GET.get("guid")
    value=request.GET.get("value")
    if not (guid and value):
        return HttpResponse("缺少GUID或者value!")
    print(timezone.localtime())
    meter_data.objects.create(meterGUID=guid, value=value, timestamp=timezone.localtime())
    return HttpResponse("200")

#labdb/retrive?guid=
@login_required(login_url="/login/")
def getMeterData(request):
    guid=request.GET.get("guid")
    if not guid:
        return HttpResponse("没有给GUID")
    retriveData=meter_data.objects.all().filter(meterGUID=guid).order_by("timestamp")
    filteredData={"meterData":[],"meterName":meter_config.objects.all().get(meterGUID=guid).meterName}
    retriveData=retriveData.filter(timestamp__gt=timezone.now()-timezone.timedelta(minutes=30))
    for meter in retriveData:
        filteredData["meterData"].append({
            "value":meter.value,
            "time":timezone.make_naive(meter.timestamp)
        })
    return JsonResponse(filteredData)

