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
from . import platforms
from .forms import AWS_AuthForm
from django import forms
import json
from .models import aws_data
import ast
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
            print(platform)
            #cloud = platforms.aws.aws(aws_access_key_id, aws_access_key)
            return redirect('aws_login/')
        else:
            print("Unsupported platform")
            return redirect('index/')

        return redirect('aws_login/')

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
        return render(request, self.template, context)

    def post(self, request):
        context = {}
        user_selection = request.POST.getlist('box')
        files_to_download = []
        print()
        print(user_selection)
        print()
        for file in user_selection:
            json_acceptable_string = file.replace("'", '"')
            #print(json_acceptable_string)
            #json_acceptable_string = str(json_acceptable_string)
            #files_to_download.append(json.loads(r"json_acceptable_string"))
            #file = r"+file
            files_to_download.append(ast.literal_eval(file))
            #if cloud == 'google':
            #    google.GDriveDownloader_add_file_to_download(file)
            #print(files_to_download)
        context['files'] = files_to_download
        if cloud == 'google':
            google.GDriveDownloader_files_to_download = files_to_download
            google.GDriveDownloader__download_File()
        return render(request, self.success_template, context)


class Aws_Buckets(View):
    template = 'cloud_download/aws_buckets.html'

    def get(self, request):
        obj = aws_data.objects.first()
        key_id_object = aws_data._meta.get_field("aws_key_id")
        key_object = aws_data._meta.get_field("aws_key")

        aws_key_id = key_id_object.value_from_object(obj)
        aws_key= key_object.value_from_object(obj)

        aws = platforms.aws.aws(aws_key_id, aws_key)
        buckets = aws.get_buckets()
        context = {'files': buckets}
        return render(request, self.template, context)

class Aws_Login(View):
    template_name = 'cloud_download/aws_login.html'

    def get(self, request):
        form = AWS_AuthForm(request.POST)
        return render(request, self.template_name, {'form': form})
    def post(self, request):
        aws_data.objects.all().delete()
        form = AWS_AuthForm(request.POST)
        if form.is_valid():
            form.save()
            aws_key_id = form.cleaned_data.get('aws_key_id')
            aws_key = form.cleaned_data.get('aws_key')
            try:
                platforms.aws.aws(aws_key_id, aws_key).get_image_list()
                return redirect("/cloud/aws_buckets/")   
            except:
                forms.ValidationError("Incorrect username or password")    
                 

        else:
            form = AWS_AuthForm()

        return render(request, self.template_name, {'form': form})

def index_redirect(request):
    return redirect('index/')

