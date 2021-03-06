# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.http import HttpResponse
from django import template
from django.db.models import Q, Sum
from django.utils import timezone
from .models import PencatatanBus
from .models import Bus
from .forms import PencatatanBusForm, EditPencatatanBusForm
from .forms import BusForm
import logging
import csv
from itertools import chain
from json import dumps
from bootstrap_datepicker_plus import DateTimePickerInput
import datetime


@login_required(login_url="/login/")
def index(request):
    bus_tiba = PencatatanBus.objects.filter(Q(keterangan='TIBA')).count()
    bus_berangkat = PencatatanBus.objects.filter(
        Q(keterangan='BERANGKAT')).count()
    bus_lintas = PencatatanBus.objects.filter(Q(keterangan='LINTAS')).count()
    data_penumpang = PencatatanBus.objects.aggregate(
        penumpang_naik=Sum('penumpang_naik'),
        penumpang_turun=Sum('penumpang_turun'),
        penumpang_datang=Sum('penumpang_datang'),
        penumpang_berangkat=Sum('penumpang_berangkat'))

    dataDictionary = {
        'bus_tiba': bus_tiba,
        'bus_berangkat': bus_berangkat,
        'bus_lintas': bus_lintas,
    }

    dataJSON = dumps(dataDictionary)
    return render(request,
                  'app/index.html',
                  context={
                      'data_bus': dataJSON,
                      'data_penumpang': data_penumpang
                  })


def public(request):
    bus_tiba = PencatatanBus.objects.filter(Q(keterangan='TIBA')).count()
    bus_berangkat = PencatatanBus.objects.filter(
        Q(keterangan='BERANGKAT')).count()
    bus_lintas = PencatatanBus.objects.filter(Q(keterangan='LINTAS')).count()
    data_penumpang = PencatatanBus.objects.aggregate(
        penumpang_naik=Sum('penumpang_naik'),
        penumpang_turun=Sum('penumpang_turun'),
        penumpang_datang=Sum('penumpang_datang'),
        penumpang_berangkat=Sum('penumpang_berangkat'))

    dataDictionary = {
        'bus_tiba': bus_tiba,
        'bus_berangkat': bus_berangkat,
        'bus_lintas': bus_lintas,
    }

    dataJSON = dumps(dataDictionary)
    return render(request,
                  'app/public.html',
                  context={
                      'data_bus': dataJSON,
                      'data_penumpang': data_penumpang
                  })


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


# @login_required(login_url="/login/")
# def barat_timur(request):
#     context = {}

#     data_pencatatan_bus = PencatatanBus.objects.filter(
#         jenis="BT").order_by('-created_at')
#     print(data_pencatatan_bus)
#     # logging.info(data_pencatatan_bus)
#     context['data_pencatatan_bus'] = data_pencatatan_bus

#     html_template = loader.get_template('app/barat-timur.html')
#     return HttpResponse(html_template.render(context, request))

# @login_required(login_url="/login/")
# def timur_barat(request):
#     context = {}

#     data_pencatatan_bus = PencatatanBus.objects.all().filter(
#         jenis="TB").order_by('-created_at')
#     print(data_pencatatan_bus)
#     # logging.info(data_pencatatan_bus)
#     context['data_pencatatan_bus'] = data_pencatatan_bus

#     html_template = loader.get_template('app/timur-barat.html')
#     return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def list_data_bus(request):
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
    bus = get_object_or_404(Bus, pk=pk)
    form = BusForm(request.POST or None, instance=bus)
    if form.is_valid():
        form.save()
        return redirect('/app/data-bus')
    return render(request, 'app/edit-data-bus.html', {'form': form})


@login_required(login_url="/login/")
def delete_data_bus(request, pk):
    print('masuk sini')
    obj = get_object_or_404(Bus, id=pk)
    if (request.method == 'POST'):
        obj.delete()
        return redirect('/app/data-bus')
    context = {'bus': obj}
    return render(request, 'app/delete-data-bus.html', context)


@login_required(login_url="/login/")
def list_pencatatan_bus(request):
    jenis = request.GET.get('jenis', '')
    start_date = request.GET.get('start_date', '')
    end_date = request.GET.get('end_date', '')

    context = {}

    data_pencatatan_bus = PencatatanBus.objects.order_by('-created_at')

    if (jenis):
        context['jenis'] = jenis
        data_pencatatan_bus = data_pencatatan_bus.filter(jenis=jenis)

    if (start_date and end_date):
        context['start_date'] = start_date
        context['end_date'] = end_date
        data_pencatatan_bus = data_pencatatan_bus.filter(
            created_at__range=(start_date, end_date))

    print(data_pencatatan_bus)
    # logging.info(data_pencatatan_bus)
    context['data_pencatatan_bus'] = data_pencatatan_bus

    html_template = loader.get_template('app/list-pencatatan-bus.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def add_pencatatan_bus(request):
    jenis = request.GET.get('jenis', '')

    if request.method == 'POST':
        form = PencatatanBusForm(request.POST)
        if form.is_valid():
            form.save()
            if (jenis):
                return redirect('/app/pencatatan-bus?jenis=' + jenis)
            return redirect('/app/pencatatan-bus')

    form = PencatatanBusForm()
    form.fields['waktu_datang'].widget = DateTimePickerInput()
    form.fields['waktu_datang'].initial = timezone.now
    form.fields['keterangan'].initial = 'LINTAS'

    if (jenis):
        form.fields['jenis'].initial = jenis

    # DateInput = partial(form.DateInput, {'class': 'datepicker'})

    print(form)

    return render(request, 'app/add-pencatatan-bus.html', {'form': form})


@login_required(login_url="/login/")
def edit_pencatatan_bus(request, pk):
    pencatatan_bus = get_object_or_404(PencatatanBus, pk=pk)
    form = EditPencatatanBusForm(request.POST or None, instance=pencatatan_bus)
    if form.is_valid():
        form.save()
        return redirect('/app/pencatatan-bus?jenis=' + pencatatan_bus.jenis)

    form.fields['waktu_datang'].widget = DateTimePickerInput()
    form.fields['waktu_berangkat'].widget = DateTimePickerInput()

    return render(request, 'app/edit-pencatatan-bus.html', {'form': form})


@login_required(login_url="/login/")
def delete_pencatatan_bus(request, pk):
    jenis = request.GET.get('jenis', '')

    obj = get_object_or_404(PencatatanBus, id=pk)
    if (request.method == 'POST'):
        print('masukkkkkkkkkkkk##')
        obj.delete()

        if (jenis):
            return redirect('/app/pencatatan-bus?jenis=' + jenis)
        return redirect('/app/pencatatan-bus')

    context = {'pencatatan_bus': obj, 'jenis': jenis}
    return render(request, 'app/delete-pencatatan-bus.html', context)


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
def export_pencatatan_bus(request):
    response = HttpResponse(content_type='text/csv')

    jenis = request.GET.get('jenis', '')
    start_date = request.GET.get('start_date', '')
    end_date = request.GET.get('end_date', '')

    writer = csv.writer(response)
    writer.writerow([
        'Nama PO', 'Plat No', 'Jenis Trayek', 'Jumlah Kursi',
        'Asal Tujuan Trayek', 'Waktu Kedatangan', 'Waktu Keberangkatan',
        'Penumpang Datang', 'Penumpang Turun', 'Penumpang Naik',
        'Penumpang Berangkat', 'Keterangan'
    ])

    data_pencatatan_bus = PencatatanBus.objects.all().values_list(
        'bus__nama_po', 'bus__plat_no', 'jenis', 'bus__jumlah_kursi',
        'bus__asal_tujuan_trayek', 'waktu_datang', 'waktu_berangkat',
        'penumpang_datang', 'penumpang_turun', 'penumpang_naik',
        'penumpang_berangkat', 'keterangan')

    if (jenis):
        data_pencatatan_bus = data_pencatatan_bus.filter(jenis=jenis)

    if (start_date and end_date):
        data_pencatatan_bus = data_pencatatan_bus.filter(
            created_at__range=(start_date, end_date))

    for pencatatan_bus in data_pencatatan_bus:
        writer.writerow(pencatatan_bus)

    response[
        'Content-Disposition'] = f'attachment; filename="Pencatatan Bus {jenis} {start_date} - {end_date}.csv"'

    return response


# @login_required(login_url="/login/")
# def exportbt(request):
#     response = HttpResponse(content_type='text/csv')

#     writer = csv.writer(response)
#     writer.writerow([
#         'Nama PO', 'Plat No', 'Jenis Trayek', 'Jumlah Kursi',
#         'Asal Tujuan Trayek', 'Waktu Kedatangan', 'Waktu Keberangkatan',
#         'Penumpang Datang', 'Penumpang Turun', 'Penumpang Naik',
#         'Penumpang Berangkat', 'Keterangan'
#     ])

#     data_pencatatan_bus_bt = PencatatanBus.objects.all().filter(
#         jenis="BT").values_list('bus__nama_po', 'bus__plat_no', 'jenis',
#                                 'bus__jumlah_kursi', 'bus__asal_tujuan_trayek',
#                                 'waktu_datang', 'waktu_berangkat',
#                                 'penumpang_datang', 'penumpang_turun',
#                                 'penumpang_naik', 'penumpang_berangkat',
#                                 'keterangan')

#     for exportbt in data_pencatatan_bus_bt:
#         writer.writerow(exportbt)

#     response[
#         'Content-Disposition'] = 'attachment; filename="Pencatatan Bus Barat Timur.csv"'

#     return response

# @login_required(login_url="/login/")
# def exporttb(request):
#     response = HttpResponse(content_type='text/csv')

#     writer = csv.writer(response)
#     writer.writerow([
#         'Nama PO', 'Plat No', 'Jenis Trayek', 'Jumlah Kursi',
#         'Asal Tujuan Trayek', 'Waktu Kedatangan', 'Waktu Keberangkatan',
#         'Penumpang Datang', 'Penumpang Turun', 'Penumpang Naik',
#         'Penumpang Berangkat', 'Keterangan'
#     ])

#     data_pencatatan_bus_tb = PencatatanBus.objects.all().filter(
#         jenis="TB").values_list('bus__nama_po', 'bus__plat_no', 'jenis',
#                                 'bus__jumlah_kursi', 'bus__asal_tujuan_trayek',
#                                 'waktu_datang', 'waktu_berangkat',
#                                 'penumpang_datang', 'penumpang_turun',
#                                 'penumpang_naik', 'penumpang_berangkat',
#                                 'keterangan')

#     for exporttb in data_pencatatan_bus_tb:
#         writer.writerow(exporttb)

#     response[
#         'Content-Disposition'] = 'attachment; filename="Pencatatan Bus Timur Barat.csv"'

#     return response
