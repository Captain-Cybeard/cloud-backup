#!/usr/bin/env python3

""" Cloud Platforms Module

Application:     Cloud Backup
File:                 /cloud_backup/cloud_download/platforms/__init__.py
Description:    Platform module initializer
Language:       Python 3.8 Django 2.2
Dev Env:         Linux x64

Authors:          Ryan Breitenfeldt
                        Noah Farris
                        Trevor Surface
                        Kyle Thomas
Class:              CptS 421/423 Fall '19 Spring '20
University:    Washington State University Tri-CIties
"""

from . import dropbox_script, gDriveDownloader, Api_keys, aws


__authors__ = ['Ryan Breitenfeldt', 'Noah Farris', 'Trevor Surface', 'Kyle Thomas']
