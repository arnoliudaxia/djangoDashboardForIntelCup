import csv
import datetime
import uuid

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import HttpResponse

from apps.labdbAPI.models import *


# labdb/meterconfig
# labdb/meterconfig?lab=
@login_required(login_url="/login/")
def getmeterConfig(request):
    configs = meter_config.objects.all()
    if request.GET.get('lab') is not None:
        configs = configs.filter(belongLab=request.GET.get('lab'))
    meters_json = {"meters": [], "labels": ["表GUID", "表名", "所属实验室"]}
    for meter in configs:
        meters_json["meters"].append({
            "meterGUID": meter.meterGUID,
            "meterName": meter.meterName,
            "belongLab": meter.belongLab
        })
    print(meters_json)

    return JsonResponse(meters_json)


# labdb/labsconfig
@login_required(login_url="/login/")
def getlabsConfig(request):
    configs = lab_config.objects.all()
    labs_json = {"labs": [], "labels": ["id", "实验室名"]}
    for lab in configs:
        labs_json["labs"].append({
            "id": lab.id,
            "labName": lab.labName
        })
    return JsonResponse(labs_json)


# labdb/register
@login_required(login_url="/login/")
def registerMeter(request):
    metername = request.GET.get("name")
    belong2Lab = request.GET.get("lab")
    if metername and belong2Lab:
        meter_config.objects.create(meterName=metername, meterGUID=str(uuid.uuid1()), belongLab=belong2Lab)
        return HttpResponse("注册表成功")
    else:
        return HttpResponse("没有写表名或所属实验室！")


# labdb/registerLab?name=实验室名
@login_required(login_url="/login/")
def registerLab(request):
    labname = request.GET.get("name")
    if labname:
        if lab_config.objects.all().filter(labName=labname).count() > 0:
            return HttpResponse("实验室已存在！")
        lab_config.objects.create(labName=labname)
        return HttpResponse("200")
    else:
        return HttpResponse("没有写实验室名！")


# labdb/remove
@login_required(login_url="/login/")
def removeMeter(request):
    guid = request.GET.get("guid")
    if guid:
        if meter_config.objects.all().filter(meterGUID=guid).count() == 1:
            meter_config.objects.all().get(meterGUID=guid).delete()
        else:
            return HttpResponse("没有找到这个表！")
        return HttpResponse("200")
    else:
        return HttpResponse("没有写表GUID！")


# labdb/removeLab?name=实验室名
@login_required(login_url="/login/")
def removeLab(request):
    labname = request.GET.get("name")
    if labname:
        if lab_config.objects.all().filter(labName=labname).count() == 1:
            lab_config.objects.all().get(labName=labname).delete()
        else:
            return HttpResponse("没有找到这个实验室！")
        return HttpResponse("200")
    else:
        return HttpResponse("没有提供实验室名！")


# labdb/record?guid=&value=
@login_required(login_url="/login/")
def record(request):
    guid = request.GET.get("guid")
    value = request.GET.get("value")
    if not (guid and value):
        return HttpResponse("缺少GUID或者value!")
    print(timezone.localtime())
    meter_data.objects.create(meterGUID=guid, value=value, timestamp=timezone.localtime())
    return HttpResponse("200")


# labdb/retrive?guid=&nearseconds=
# 获取guid表的所有数据，如果给定nearseconds，则只获取nearseconds 秒内的数据
@login_required(login_url="/login/")
def getMeterData(request):
    guid = request.GET.get("guid")
    nearseconds = int(request.GET.get("nearseconds"))
    if not guid:
        return HttpResponse("没有给GUID")
    retriveData = meter_data.objects.filter(meterGUID=guid)
    filteredData = {"meterData": [], "meterName": meter_config.objects.all().get(meterGUID=guid).meterName}
    if nearseconds > 0:
        #     # 这个时区的问题实在是太烦人了，不知道为啥从mySQL读取的时区是UTC时间，晕了
        retriveData = retriveData.filter(
            timestamp__gt=timezone.localtime() - datetime.timedelta(seconds=nearseconds) + datetime.timedelta(hours=8))

    # print("查询到的数据一共有：",retriveData.count())

    for meter in retriveData:
        filteredData["meterData"].append({
            "value": meter.value,
            "time": meter.timestamp
        })
    return JsonResponse(filteredData)


# labdb/preview/$pid$
# 获取进程号为pid的AI实时的result img
@login_required(login_url="/login/")
def preview(request, pid: int):
    return HttpResponse(ai_process.objects.get(pid=pid).previewImage)


# labdb/export/$guid$
# 将表的所有数据导出出去
@login_required(login_url="/login/")
def export(request, guid: int):
    meterName = meter_config.objects.get(meterGUID=guid).meterName
    fileName = f"{meterName}_{guid}.csv"

    response = HttpResponse(
        content_type='text/csv',
        headers={'Content-Disposition': f'attachment; filename=\"{fileName}\"'},
    )
    writer = csv.writer(response)
    dataCollector = meter_data.objects.filter(meterGUID=guid)
    for data in dataCollector:
        writer.writerow([meterName,data.meterGUID,data.timestamp, data.value])

    return response
