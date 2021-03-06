# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.
OPSI_JENIS_PENCATATAN = [
    ("BT", "BT"),
    ("TB", "TB"),
]

OPSI_KETERANGAN = [
    ("LINTAS", "LINTAS"),
    ("BERANGKAT", "BERANGKAT"),
    ("TIBA", "TIBA"),
]

OPSI_JENIS_TRAYEK = [
    ("AKAP", "AKAP"),
    ("AKDP", "AKDP"),
    ("ANGKT", "ANGKT"),
]


class TimeStampMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Bus(models.Model):
    nama_po = models.CharField(max_length=20)
    plat_no = models.CharField(max_length=10)
    jenis_trayek = models.CharField(max_length=5, choices=OPSI_JENIS_TRAYEK)
    jumlah_kursi = models.PositiveIntegerField(default=0)
    asal_tujuan_trayek = models.CharField(max_length=50)

    class Meta:
        db_table = "app_bus"

    def __str__(self):
        return self.nama_po + ' - ' + self.plat_no


class PencatatanBus(TimeStampMixin):
    jenis = models.CharField(max_length=2, choices=OPSI_JENIS_PENCATATAN)
    waktu_datang = models.DateTimeField()
    waktu_berangkat = models.DateTimeField(default=timezone.now)
    penumpang_datang = models.PositiveIntegerField()
    penumpang_naik = models.PositiveIntegerField()
    penumpang_turun = models.PositiveIntegerField()
    penumpang_berangkat = models.PositiveIntegerField()
    keterangan = models.CharField(max_length=10, choices=OPSI_KETERANGAN)
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE)
