# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from travelmobApp.models import ScrapModel, ScrapDetails


# Resources
class ScrapModelResource(resources.ModelResource):
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
admin.site.register(ScrapDetails)
