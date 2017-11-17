# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from travelmobApp.models import ScrapModel, ScrapDetails

admin.site.register(ScrapModel)
admin.site.register(ScrapDetails)