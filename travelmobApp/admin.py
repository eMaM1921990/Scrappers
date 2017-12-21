# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from import_export import fields
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from import_export.fields import Field

from travelmobApp.models import ScrapModel, ScrapDetails


# Resources
class ScrapModelResource(resources.ModelResource):
    count_all_number = fields.Field(attribute='count_has_numbers')
    count_all_record = fields.Field(attribute='count_all')

    class Meta:
        model = ScrapModel
        skip_unchanged = True


class ScapperAdmin(ImportExportModelAdmin):
    list_display = ['id', 'name', 'source', 'count_has_numbers', 'count_all']

    list_per_page = 10
    search_fields = ('id', 'name', 'source',)

    resource_class = ScrapModelResource

    class Meta:
        verbose_name = 'City Scrapper'
        verbose_name_plural = 'City Scrapper'


admin.site.register(ScrapModel, ScapperAdmin)


# Resources
class ScrapDetailsResource(resources.ModelResource):

    class Meta:
        model = ScrapDetails
        skip_unchanged = True
        fields = ['id', 'name', 'f_name', 'l_name', 'phone', 'url', 'scrap__name']


class ScapperDetailsAdmin(ImportExportModelAdmin):
    list_display = ['id', 'name', 'f_name', 'l_name', 'phone', 'url', 'scrap']

    list_per_page = 10
    search_fields = ('id', 'name', 'f_name', 'l_name', 'phone',)

    resource_class = ScrapDetailsResource

    class Meta:
        verbose_name = 'City Scrapper Details'
        verbose_name_plural = 'City Scrapper Details'


admin.site.register(ScrapDetails, ScapperDetailsAdmin)
