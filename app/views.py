# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.http import HttpResponse
from django import template
from .models import PencatatanBus
from .models import Bus
from .forms import PencatatanBusForm
from .forms import BusForm
import logging
import csv
from itertools import chain


@login_required(login_url="/login/")
def index(request):

    # context = {}
    # context['segment'] = 'index'

    # html_template = loader.get_template('index.html')
    # return HttpResponse(html_template.render(context, request))

    return redirect("/app/index.html")


@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split('/')[-1]
        context['segment'] = load_template

        html_template = loader.get_template(load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:

        html_template = loader.get_template('page-500.html')
        return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def app_home(request):

    context = {}
    context['segment'] = 'app_home'

    html_template = loader.get_template('app/index.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def app_pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split('/')[-1]
        context['segment'] = load_template

        html_template = loader.get_template('app/' + load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:

        html_template = loader.get_template('page-500.html')
        return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def barat_timur(request):
    context = {}

    data_pencatatan_bus = PencatatanBus.objects.filter(
        jenis="BT").order_by('-created_at')
    print(data_pencatatan_bus)
    # logging.info(data_pencatatan_bus)
    context['data_pencatatan_bus'] = data_pencatatan_bus

    html_template = loader.get_template('app/barat-timur.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def timur_barat(request):
    context = {}

    data_pencatatan_bus = PencatatanBus.objects.all().filter(
        jenis="TB").order_by('-created_at')
    print(data_pencatatan_bus)
    # logging.info(data_pencatatan_bus)
    context['data_pencatatan_bus'] = data_pencatatan_bus

    html_template = loader.get_template('app/timur-barat.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def pencarian_bus(request):
    context = {}
    data_pencarian_bus = Bus.objects.all()
    print(data_pencarian_bus)
    # logging.info(data_pencatatan_bus)
    context['data_pencarian_bus'] = data_pencarian_bus
    html_template = loader.get_template('app/data-bus.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def add_bus(request):
    if request.method == 'POST':
        form = BusForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/app/data-bus.html')
    form = BusForm()

    print(form)

    return render(request, 'app/add-data-bus.html', {'form': form})


@login_required(login_url="/login/")
def edit_bus(request, pk):
    print('masukkkkk')
    bus = get_object_or_404(Bus, pk=pk)
    form = BusForm(request.POST or None, instance=bus)
    if form.is_valid():
        form.save()
        return redirect('/app/data-bus.html')
    return render(request, 'app/edit-data-bus.html', {'form': form})


@login_required(login_url="/login/")
def add_pencatatan_bus(request):
    if request.method == 'POST':
        form = PencatatanBusForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/app/barat-timur.html')
    form = PencatatanBusForm()

    print(form)

    return render(request, 'app/add-pencatatan-bus.html', {'form': form})


@login_required(login_url="/login/")
def edit_pencatatan_bus(request, pk):
    # return HttpResponse("You're looking at question %s." % pk)
    print('masukkkkk')
    pencatatan_bus = get_object_or_404(PencatatanBus, pk=pk)
    form = PencatatanBusForm(request.POST or None, instance=pencatatan_bus)
    if form.is_valid():
        form.save()
        return redirect('/app/barat-timur.html')
    return render(request, 'app/edit-pencatatan-bus.html', {'form': form})


@login_required(login_url="/login/")
def exportbus(request):
    response = HttpResponse(content_type='text/csv')

    writer = csv.writer(response)
    writer.writerow([
        'Nama PO',
        'Plat No',
        'Jenis Trayek',
        'Jumlah Kursi',
        'Asal Tujuan Trayek',
    ])

    for bus in Bus.objects.all().values_list('nama_po', 'plat_no',
                                             'jenis_trayek', 'jumlah_kursi',
                                             'asal_tujuan_trayek'):
        writer.writerow(bus)

    response['Content-Disposition'] = 'attachment; filename="Data Bus.csv"'

    return response


@login_required(login_url="/login/")
def exportbt(request):
    response = HttpResponse(content_type='text/csv')

    writer = csv.writer(response)
    writer.writerow([
        'Nama PO', 'Plat No', 'Jenis Trayek', 'Jumlah Kursi',
        'Asal Tujuan Trayek', 'Waktu Kedatangan', 'Waktu Keberangkatan',
        'Penumpang Datang', 'Penumpang Turun', 'Penumpang Naik',
        'Penumpang Berangkat', 'Keterangan'
    ])

    data_pencatatan_bus_bt = PencatatanBus.objects.all().filter(
        jenis="BT").values_list('bus__nama_po', 'bus__plat_no', 'jenis',
                                'bus__jumlah_kursi', 'bus__asal_tujuan_trayek',
                                'waktu_datang', 'waktu_berangkat',
                                'penumpang_datang', 'penumpang_turun',
                                'penumpang_naik', 'penumpang_berangkat',
                                'keterangan')

    for exportbt in data_pencatatan_bus_bt:
        writer.writerow(exportbt)

    response[
        'Content-Disposition'] = 'attachment; filename="Pencatatan Bus Barat Timur.csv"'

    return response


@login_required(login_url="/login/")
def exporttb(request):
    response = HttpResponse(content_type='text/csv')

    writer = csv.writer(response)
    writer.writerow([
        'Nama PO', 'Plat No', 'Jenis Trayek', 'Jumlah Kursi',
        'Asal Tujuan Trayek', 'Waktu Kedatangan', 'Waktu Keberangkatan',
        'Penumpang Datang', 'Penumpang Turun', 'Penumpang Naik',
        'Penumpang Berangkat', 'Keterangan'
    ])

    data_pencatatan_bus_tb = PencatatanBus.objects.all().filter(
        jenis="TB").values_list('bus__nama_po', 'bus__plat_no', 'jenis',
                                'bus__jumlah_kursi', 'bus__asal_tujuan_trayek',
                                'waktu_datang', 'waktu_berangkat',
                                'penumpang_datang', 'penumpang_turun',
                                'penumpang_naik', 'penumpang_berangkat',
                                'keterangan')

    for exporttb in data_pencatatan_bus_tb:
        writer.writerow(exporttb)

    response[
        'Content-Disposition'] = 'attachment; filename="Pencatatan Bus Timur Barat.csv"'

    return response