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
University:    Washington State University Tri-Cities
"""

from django.shortcuts import render, redirect
from django.views import View
import json
from . import platforms

__authors__ = ['Ryan Breitenfeldt', 'Noah Farris', 'Trevor Surface', 'Kyle Thomas']

##############################
global cloud, dropbox #Need to add the other platforms as needed
cloud = ""
dropbox = platforms.dropbox_script.DropBox()
##############################

class Index(View):
    index_template = 'cloud_download/index.html'
    platforms = ['google', 'dropbox', 'aws']

    def get(self, request):
        context = {'platforms': self.platforms}
        return render(request, self.index_template, context)

    def post(self, request):
        platform = request.POST['platform']
        global cloud
        if platform == 'google':
            print(platform)  # DEBUGGING
            cloud = platforms.gDriveDownloader.GDriveDownloader()
        ############################
        elif platform == 'dropbox': #The following are the recomended changes
            cloud = 'dropbox' #For the Files class
            return redirect('dropbox-auth-start/') #Calls the dropbox authentication
        ############################
        elif platform == 'aws':
            print(platform)  # DEBUGGING
        else:
            print("Unsupported platform")
            return redirect('index/')

        return redirect('files/')

class Files(View):
    template = 'cloud_download/files.html'
    success_template = 'cloud_download/success.html'
    #global cloud
    def get(self, request):
        ######################################
        if cloud == 'dropbox': #Checks value set by Index class 
            context = dropbox.dropbox_format_json #Uses dropbox class to see data
        ######################################
        print(context)
        return render(request, self.template, context)

    def post(self, request):
        files_to_download = request.POST['box']  # The user selected items
        print(files_to_download)
        return render(request, self.success_template, files_to_download)

def index_redirect(request):
    return redirect('index/cloud')
