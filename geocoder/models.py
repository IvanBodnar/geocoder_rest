# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals
from django.db import models
from django.contrib.postgres.fields import IntegerRangeField
from django.contrib.gis.db import models


class CallesGeocod(models.Model):
    id = models.IntegerField(primary_key=True)
    codigo = models.IntegerField(blank=True, null=True)
    nombre = models.CharField(max_length=50, blank=True, null=True)
    alt_i = models.IntegerField(blank=True, null=True)
    alt_f = models.IntegerField(blank=True, null=True)
    tipo = models.CharField(max_length=50, blank=True, null=True)
    geom = models.MultiLineStringField(blank=True, null=True, srid=4326)
    geom_3857 = models.MultiLineStringField(blank=True, null=True, srid=3857)
    rango = IntegerRangeField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'calles_geocod'
