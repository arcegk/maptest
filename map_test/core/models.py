from django.db import models


class Address(models.Model):
    lat = models.CharField(max_length=100, verbose_name='latitude')
    lon = models.CharField(max_length=100, verbose_name='longitude')
    address = models.CharField(max_length=125, verbose_name='address')

    def __str__(self):
        return f'{self.lat}, {self.lon} - {self.address}'


class FusionTable(models.Model):
    table_id = models.CharField(max_length=200, verbose_name='table id')
