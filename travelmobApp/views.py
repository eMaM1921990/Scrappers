# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import openpyxl
from openpyxl.utils import get_column_letter

from travelmobApp.SalesForce import  SalesForceClass

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
    data = ScrapDetails.objects.filter(name__isnull=False).values('name','scrap__name','phone').annotate(total=Count('id')).order_by('-total')
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="property.csv"'
    writer = csv.writer(response)
    field_names = ["Manager name ", 'Location','count']
    writer.writerow(field_names)
    for row in data:
        if len(row['name'].encode('utf-8').strip())>0:

             writer.writerow([row['name'].encode('utf-8').strip(), row['scrap__name'].encode('utf-8').strip(),row['phone'], row['total']])
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


def cloneSalesForceLeads(request):
    SalesForce = SalesForceClass()
    # SalesForce.check_and_create_lead(
    #     last_name='(Fake do not process) Joe & Mathers Fava',
    #     phone='16268645227',
    #     campaign_source='Panama City, FL',
    #     lead_source='Flipkey Website',
    #     website='https://www.flipkey.com/properties/8801586/',
    #     company='Flipkey',
    #     tags='flipkey, scrape, house',
    #     is_international=True
    # )

    sales_force_leads_list  = SalesForce.query_all_leads()
    return sales_force_leads_list