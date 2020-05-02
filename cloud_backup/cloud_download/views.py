#!/usr/bin/env python3

""" URL views for cloud backup application
Application:    Cloud Backup
File:           /cloud_backup/cloud_download/views.py
Description:    Django Views / web pages
Language:       Python 3.8 Django 2.2
Dev Env:        Linux x64

Authors:        Ryan Breitenfeldt
                Noah Farris
                Trevor Surface
                Kyle Thomas
Class:          CptS 421/423 Fall '19 Spring '20
University:     Washington State University Tri-Cities
"""

import ast
from django.shortcuts import render, redirect
from django.views import View
from . import platforms
from .forms import AWS_AuthForm
from django import forms
import json
from .models import aws_data
import ast
from django.contrib import messages

__authors__ = ['Ryan Breitenfeldt', 'Noah Farris', 'Trevor Surface', 'Kyle Thomas']

# Globals to set the cloud platform
global cloud, dropbox  # Need to add the other platforms as needed
cloud = ""
dropbox = platforms.dropbox_script.DropBox()
google = platforms.gDriveDownloader.GDriveDownloader()


class Index(View):
    """The index view is the main page where the user selects the platform."""
    index_template = 'cloud_download/index.html'
    platforms = ['google', 'dropbox', 'aws']

    def get(self, request):
        """get method to display available platforms."""
        context = {'platforms': self.platforms}
        return render(request, self.index_template, context)

    def post(self, request):
        """post method collects the user selected platform and invokes the correct platform object."""
        platform = request.POST['platform']
        global cloud
        if platform == 'google':
            cloud = 'google'
            return redirect('google-auth-start/')
        elif platform == 'dropbox':
            cloud = 'dropbox'
            return redirect('dropbox-auth-start/')
        elif platform == 'aws':
            cloud = 'aws'
            return redirect('aws_login/')
        else:
            print("Unsupported platform")
            return redirect('index/')

        return redirect('aws_login/')


class Files(View):
    """The Files class is the view for displaying the user's files"""
    template = 'cloud_download/files.html'
    success_template = 'cloud_download/success.html'

    def get(self, request):
        """get will display the files to select for the user"""

        # Determine platform and get files from that platform
        if cloud == 'dropbox':
            context = dropbox.dropbox_format_json
        elif cloud == 'google':
            context = google.GDriveDownloader_json
        elif cloud == 'aws':
            obj = aws_data.objects.first()
            key_id_object = aws_data._meta.get_field("aws_key_id")
            key_object = aws_data._meta.get_field("aws_key")
            aws_key_id = key_id_object.value_from_object(obj)
            aws_key= key_object.value_from_object(obj)
            aws = platforms.aws.aws(aws_key_id, aws_key)
            return render(request, self.template, {'files': aws.list_images_in_bucket()})
        return render(request, self.template, context)

    def post(self, request):
        """post gathers what the user selected for files and downloads the files from the platform onto the server."""
        if cloud == 'aws':
            obj = aws_data.objects.first()
            key_id_object = aws_data._meta.get_field("aws_key_id")
            key_object = aws_data._meta.get_field("aws_key")
            aws_key_id = key_id_object.value_from_object(obj)
            aws_key= key_object.value_from_object(obj)
            aws = platforms.aws.aws(aws_key_id, aws_key)
            context = {}
            user_selection = request.POST.getlist('box')
            files_to_download = []
            for file in user_selection:
                file_name = ast.literal_eval(file)
                aws.download_image('testbucket1293248523850923853', file_name['name'])
                json_acceptable_string = file.replace("'", "\"")
                files_to_download.append(json.loads(json_acceptable_string))
            context['files'] = files_to_download
            return render(request, self.success_template, context)
        elif cloud == 'google':
            context = {}
            user_selection = request.POST.getlist('box')
            files_to_download = []

            for file in user_selection:
                files_to_download.append(ast.literal_eval(file))
            context['files'] = files_to_download
            if cloud == 'google':
                google.GDriveDownloader_files_to_download = files_to_download
                google.GDriveDownloader__download_File()
            return render(request, self.success_template, context)

class Aws_Login(View):
    """Aws_Login is the view for authenticating the user to AWS."""
    template_name = 'cloud_download/aws_login.html'

    def get(self, request):
        """get displays the form to the user to authenticate to AWS"""
        form = AWS_AuthForm(request.POST)
        return render(request, self.template_name, {'form': form})
        
    def post(self, request):
        """post takes in the user's credentials and uses those to authenticate to AWS"""
        aws_data.objects.all().delete()
        form = AWS_AuthForm(request.POST)
        if form.is_valid():
            form.save()
            aws_key_id = form.cleaned_data.get('aws_key_id')
            aws_key = form.cleaned_data.get('aws_key')
            try:
                platforms.aws.aws(aws_key_id, aws_key).get_image_list()
                return redirect("/cloud/files/")   
            except:
                messages.error(request, 'Amazon Web Services Key or Key ID is incorrect!')                 
        else:
            form = AWS_AuthForm()
        return render(request, self.template_name, {'form': form})

#def index_redirect(request):
#    return redirect('index/')

