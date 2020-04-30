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
google = platforms.gDriveDownloader.GDriveDownloader()
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
            cloud = 'google'
            return redirect('google-auth-start/')
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

####def flatten_list(x, flat_list):
####    for file in x['files']:
####        flat_list.append(file['path'])
####    for dir in x['dirs']:
####        flatten_list(x, flat_list)
        
#a = {'path': '', 'dirs': [{'path': '/grabfiles', 'dirs': [], 'files': [{'path': '/grabfiles/.git', 'name': '.git'}, {'
#   ...: path': '/grabfiles/readme.md', 'name': 'readme.md'}, {'path': '/grabfiles/grabfiles.go', 'name': 'grabfiles.go'}]}], '
#   ...: files': [{'path': '/get started with dropbox paper.url', 'name': 'get started with dropbox paper.url'}, {'path': '/get
#   ...:  started with dropbox.pdf', 'name': 'get started with dropbox.pdf'}]}


class Files(View):
    template = 'cloud_download/files.html'
    success_template = 'cloud_download/success.html'
    #global cloud
    def get(self, request):
        ######################################
        if cloud == 'dropbox': #Checks value set by Index class 
            context = dropbox.dropbox_format_json #Uses dropbox class to see data
        ######################################
        elif cloud == 'google':
            context = google.GDriveDownloader_json

        print(context)
        return render(request, self.template, context)

    def post(self, request):
        files_to_download = request.POST['box']  # The user selected items
        print(files_to_download)  # DEBUGGING
        return render(request, self.success_template, files_to_download)

def index_redirect(request):
    return redirect('index/cloud')
