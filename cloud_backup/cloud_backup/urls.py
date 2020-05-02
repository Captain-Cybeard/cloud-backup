#!/usr/bin/env python3

""" URL views for cloud backup application
Application:    Cloud Backup
File:           /cloud_backup/cloud_backup/urls.py
Description:    Django root url directions
Language:       Python 3.8 Django 2.2
Dev Env:        Linux x64

Authors:        Ryan Breitenfeldt
                Noah Farris
                Trevor Surface
                Kyle Thomas
Class:          CptS 421/423 Fall '19 Spring '20
University:    Washington State University Tri-Cities
"""

from django.contrib import admin
from django.urls import include, path

__authors__ = ['Ryan Breitenfeldt', 'Noah Farris', 'Trevor Surface', 'Kyle Thomas']

urlpatterns = [
    path('', include('cloud_download.urls')),  # Empty path redirects to 'cloud_download' app
    path('cloud/', include('cloud_download.urls')),  # /cloud/ path redirects to 'cloud_download' app
    path('admin/', admin.site.urls),  # Default django admin
]
