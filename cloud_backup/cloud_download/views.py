#!/usr/bin/env python3

""" URL views for cloud backup application
Application:     Cloud Backup
File:                 /cloud_backup/cloud_download/views.py
Description:    Django Views / web pages
Language:       Python 3.8 Django 2.2
Dev Env:         Linux x64

Authors:          Ryan Breitenfeldt
                        Noah Farris
                        Trevor Surface
                        Kyle Thomas
Class:              CptS 421/423 Fall '19 Spring '20
University:    Washington State University Tri-CIties
"""

from django.shortcuts import render, redirect
from django.views import View
from . import platforms

__authors__ = ['Ryan Breitenfeldt', 'Noah Farris', 'Trevor Surface', 'Kyle Thomas']


class Index(View):
    index_template = 'cloud_download/index.html'

    # not sure if this is the best way to do this?
    # Will have to match if/else block in the post() method
    platforms = ['google', 'dropbox', 'aws']
    cloud = None  # the user selected cloud platform

    def get(self, request):
        context = {'platforms': self.platforms}
        return render(request, self.index_template, context)

    def post(self, request):
        platform = request.POST['platform']
        if platform == 'google':
            print(platform)  # DEBUGGING
            cloud = platforms.gDriveDownloader.GDriveDownloader()
        elif platform == 'dropbox':
            print(platform)  # DEBUGGING
            cloud = platforms.dropbox_script.DropBox()
            print(cloud)
        elif platform == 'aws':
            print(platform)  # DEBUGGING
        else:
            print("Unsupported platform")
            return redirect('index/')

        return redirect('files/')


class Files(View):
    template = 'cloud_download/files.html'

    def get(self, request):
        context = {'files': ['/home', '/home/bart', '/root', 'hello.c']}
        return render(request, self.template, context)


def index_redirect(request):
    return redirect('index/')
