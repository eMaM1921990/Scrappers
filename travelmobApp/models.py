# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import django
from django.db import models

# Create your models here.
from django.db.models.base import Model

MANAGED = True


class ScrapModel(models.Model):
    name = models.TextField()
    source = models.CharField(max_length=100, null=False , default='FlipKey')
    created_date = models.DateField(default=django.utils.timezone.now)


    @property
    def count_has_numbers(self):
        return self.scrap_model.filter(phone__isnull=False).count()

    def __unicode__(self):
        return self.name

    class Meta:
        managed = MANAGED
        db_table = 'scrap_model'


class ScrapDetails(models.Model):
    scrap = models.ForeignKey(ScrapModel, models.CASCADE, related_name='scrap_model', db_column='scrap_mode_id')
    name = models.CharField(max_length=150, null=True)
    f_name = models.CharField(max_length=150,null=True)
    l_name = models.CharField(max_length=150,null=True)
    phone = models.CharField(max_length=150,null=True)
    url = models.URLField()

    class Meta:
        managed = MANAGED
        db_table = 'scrap_details'
