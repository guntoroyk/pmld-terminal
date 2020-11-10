# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.


class Bus(models.Model):
    nama_po = models.CharField(max_length=20)
    plat_no = models.CharField(max_length=10)
    jenis_trayek = models.CharField(max_length=5)
    jumlah_kursi = models.PositiveIntegerField()
    asal_tujuan_trayek = models.CharField(max_length=50)


class PencatatanBus(models.Model):
    waktu_datang = models.DateTimeField()
    waktu_berangkat = models.DateTimeField(default=timezone.now)
    jumlah_penumpang_datang = models.PositiveIntegerField()
    penumpang_naik = models.PositiveIntegerField()
    penumpang_turun = models.PositiveIntegerField()
    jumlah_penumpang_berangkat = models.PositiveIntegerField()
    keterangan = models.CharField(max_length=10)
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE)
