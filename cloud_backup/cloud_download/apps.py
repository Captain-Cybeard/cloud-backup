#!/usr/bin/env python3

""" App declaration for cloud backup application
Application:     Cloud Backup
File:                 /cloud_backup/cloud_download/apps.py
Description:    Django App Config
Language:       Python 3.8 Django 2.2
Dev Env:         Linux x64

Authors:          Ryan Breitenfeldt
                        Noah Farris
                        Trevor Surface
                        Kyle Thomas
Class:              CptS 421/423 Fall '19 Spring '20
University:    Washington State University Tri-CIties
"""

from django.apps import AppConfig

__authors__ = ['Ryan Breitenfeldt', 'Noah Farris', 'Trevor Surface', 'Kyle Thomas']


class CloudDownloadConfig(AppConfig):
    name = 'cloud_download'
