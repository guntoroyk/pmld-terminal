# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from app import views

urlpatterns = [

    # The home page
    path('', views.index, name='home'),
    path('app', views.app_home, name='app_home'),
    path('app/add-pencatatan-bus/',
         views.add_pencatatan_bus,
         name='add_pencatatan_bus'),
    path('app/edit-pencatatan-bus/<int:pk>/',
         views.edit_pencatatan_bus,
         name='edit_pencatatan_bus'),
    re_path(r'^app/barat-timur*\.*', views.barat_timur, name='barat_timur'),
    re_path(r'^app/timur-barat*\.*', views.timur_barat, name='timur_barat'),
    re_path(r'^app/.*\.*', views.app_pages, name='app_pages'),

    # Matches any html file
    re_path(r'^.*\.*', views.pages, name='pages'),
]
