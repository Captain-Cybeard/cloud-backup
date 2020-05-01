#!/usr/bin/env python3

""" URL directs for cloud backup application
Application:    Cloud Backup
File:           /cloud_backup/cloud_download/urls.py
Description:    url paths
Language:       Python 3.8 Django 2.2
Dev Env:        Linux x64

Authors:        Ryan Breitenfeldt
                Noah Farris
                Trevor Surface
                Kyle Thomas
Class:          CptS 421/423 Fall '19 Spring '20
University:     Washington State University Tri-CIties
"""

from django.urls import path
from . import views

__authors__ = ['Ryan Breitenfeldt', 'Noah Farris', 'Trevor Surface', 'Kyle Thomas']


urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    ##############################################
    path('dropbox-auth-start/', views.dropbox.dropbox_authentication_start), #Paths added to allow auth function to run
    path('dropbox-auth-finish/', views.dropbox.dropbox_authentication_finish), #Paths added to allow auth finish to complete
    ##############################################
    path('google-auth-start/', views.google.GDriveDownloaded_authentication_start),
    path('google-auth-finish/', views.google.GDriveDownloaded_authentication_finish),
    ##############################################
    path('files/', views.Files.as_view(), name='files'),
    path('aws_login/', views.Aws_Login.as_view(), name='aws_login'),


]