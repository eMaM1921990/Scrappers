# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import openpyxl
from openpyxl.utils import get_column_letter

try:
    import cStringIO as StringIO
except ImportError:
    import StringIO
import csv
import sys

import xlsxwriter
from cities_light.models import City
from django.conf import settings
from django.db.models import Count
from django.http.response import HttpResponse
from django.shortcuts import render, redirect
import json

# Create your views here.
from django.views.decorators.http import require_http_methods

from travelmobApp.FlipKey import FlipKeyScrapper
from travelmobApp.models import ScrapModel, ScrapDetails

reload(sys)
sys.setdefaultencoding('utf8')


def index(request):
    context = {}
    template = 'index.html'
    # Get Cities
    context['cities'] = City.objects.values('name').distinct()
    return render(request, template, context=context)


def travelMobData(request):
    context = {}
    template = 'travelMobData.html'
    context['data'] = ScrapModel.objects.all()
    return render(request, template, context=context)


def exportPropertyUnitCount(request):
    # get data
    allData = ScrapDetails.objects.filter(name__isnull=False)
    data = allData.values('name', 'f_name', 'l_name', 'scrap__name','url','phone').annotate(total=Count('id')).order_by('-total')

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=PropertyManager.xlsx'
    wb = openpyxl.Workbook()
    ws = wb.get_active_sheet()
    ws.title = "URL Count"

    row_num = 0

    columns = [
        (u"Property Manager", 15),
        (u"Location", 100),

        (u"URL", 70),
        (u"Phone", 70),
        (u"Count", 70),
    ]

    for col_num in xrange(len(columns)):
        c = ws.cell(row=row_num + 1, column=col_num + 1)
        c.value = columns[col_num][0]
        # set column width
        ws.column_dimensions[get_column_letter(col_num + 1)].width = columns[col_num][1]

    for obj in data:
        row_num += 1
        row = [
            obj['name'].encode('utf-8').strip(),
            obj['scrap__name'].encode('utf-8').strip(),
            obj['url'].encode('utf-8').strip(),
            obj['phone'].encode('utf-8').strip(),
            obj['total'],
        ]
        for col_num in xrange(len(row)):
            c = ws.cell(row=row_num + 1, column=col_num + 1)
            c.value = row[col_num]


    wb.save(response)
    return response


@require_http_methods(["GET"])
def exportData(request, id, name):
    # get data
    data = ScrapDetails.objects.filter(scrap__id=id)
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="' + name + '.csv"'
    writer = csv.writer(response)
    field_names = ["name", "first_name", "last_name", "phone_number", 'url']
    writer.writerow(field_names)
    for row in data:
        writer.writerow([row.name, row.f_name, row.l_name, row.phone, row.url])

    return response


@require_http_methods(["GET"])
def exportExtraData(request, id, name, unique):
    # get data
    if unique:
        data = ScrapDetails.objects.filter(scrap__id=id, phone__isnull=False)
    else:
        data = ScrapDetails.objects.filter(scrap__id=id, phone__isnull=False)
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="' + name + '.csv"'
    writer = csv.writer(response)
    field_names = ["name", "first_name", "last_name", "phone_number", 'url']
    writer.writerow(field_names)
    for row in data:
        writer.writerow([row.name, row.f_name, row.l_name, row.phone, row.url])

    return response


@require_http_methods(["POST"])
def scrap(request):
    valid = False
    cityId = request.POST.get('city')
    website = request.POST.get('website')
    if website not in settings.WEBSITE_LIST:
        ret = {
            'valid': valid,
            'msg': 'Invalid website'
        }

        return HttpResponse(json.dumps(ret, ensure_ascii=False))
    else:
        cities = City.objects.values('name').filter(name__startswith='l').distinct()
        flipKey = FlipKeyScrapper()
        for city in cities:
            print 'start processing with city ' + str(city['name'])
            # start scrap
            flipKey.start_processing(city['name'])
            # flipKey = FlipKeyScrapper()
            # flipKey.start_processing(cityId)

    return None
