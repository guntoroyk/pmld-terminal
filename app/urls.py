# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from app import views

urlpatterns = [

    # The home page
    path('', views.index, name='home'),
    path('public', views.public, name='public'),
    path('app', views.app_home, name='app_home'),
    path('app/pencatatan-bus', views.list_pencatatan_bus),
    path('app/pencatatan-bus/add',
         views.add_pencatatan_bus,
         name='add_pencatatan_bus'),
    path('app/pencatatan-bus/<int:pk>',
         views.edit_pencatatan_bus,
         name='edit_pencatatan_bus'),
    path('app/pencatatan-bus/<int:pk>/delete',
         views.delete_pencatatan_bus,
         name='delete_pencatatan_bus'),
    path('app/data-bus', views.list_data_bus),
    path('app/data-bus/add', views.add_bus, name='add_bus'),
    path('app/data-bus/<int:pk>', views.edit_bus, name='edit_bus'),
    path('app/data-bus/<int:pk>/delete',
         views.delete_data_bus,
         name='delete_data_bus'),
    path('app/export-pencatatan-bus',
         views.export_pencatatan_bus,
         name='export-pencatatan-bus'),
    #     re_path(r'^app/barat-timur*\.*', views.barat_timur, name='barat_timur'),
    #     re_path(r'^app/timur-barat*\.*', views.timur_barat, name='timur_barat'),
    #     re_path(r'^app/data-bus*\.*', views.list_data_bus, name='data_bus'),
    re_path(r'^app/.*\.*', views.app_pages, name='app_pages'),
    #path('app/data-bus', views.pencarian_bus, 'pencarianbus'),
    path('exportbus', views.exportbus, name='exportbus'),
    #     path('exportbt', exportbt, name='exportbt'),
    #     path('exporttb', exporttb, name='exporttb'),

    # Matches any html file
    re_path(r'^.*\.*', views.pages, name='pages'),
]
