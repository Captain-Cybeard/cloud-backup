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

'''
For Admins:
    When adding a new platform to the software if the platform SDK supports OAuth2.0 authentication
    Then the new platform class will need to be instantiated bellow along with the previous OAuth2.0 
    class objects.  
'''
global cloud 
cloud = ""
dropbox = platforms.dropbox_script.DropBox()
google = platforms.gDriveDownloader.GDriveDownloader()


class Index(View):
    '''
    For Admins:
        When adding a new platform, the attribute platform will need to be updated with the new platform name.
        Additionally the post method of this class will need to be updated with elif similar to the previous functionality
        of the post method. To finalize the post method, there also needs to be a redirect to '[platform-name]-auth-start'
        To enable this as well the urls.py needs to be updated. 
    '''

    index_template = 'cloud_download/index.html'
    platforms = ['google', 'dropbox', 'aws']

    def get(self, request):
        context = {'platforms': self.platforms}
        return render(request, self.index_template, context)

    def post(self, request):
        platform = request.POST['platform']
        global cloud
        if platform == 'google':
            print(platform)  
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
    '''
    For Admins:
        The current functionality of the software requires a single level dict with the parameters {'files':[]} with a list
        of dicts containing {'path':'', 'files':''} where 'files' is the name of the file without folder names included. The classes
        are implemented with a dict that allows mulilevel folder and file view, if the developer would like to change the layout, further 
        programming is required.

        The get method of this class will need to be updated with another elif to provide the neccessary dict for the layout of the files.
    '''
    
    template = 'cloud_download/files.html'
    success_template = 'cloud_download/success.html'
    context = {}
    def get(self, request):
        if cloud == 'dropbox':  
            context = dropbox.dropbox_flat_dict 
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
        '''
        For admins
            This method needs to be updated when a new platform is added regardless of Oauth2 authentication 
            This is what calls the download procedures defined within the new platform class. Any additional
            information needed for downloading will need to be added to the context list and the information
            transfered. Add an elif case for the new platform with a similar for loop consitant with the other
            if statements, then call the download funciton neccessary for the platform.
        '''
        
        context = {}
        user_selection = request.POST.getlist('box')
        files_to_download = []
        
        if cloud == 'aws':
            obj = aws_data.objects.first()
            key_id_object = aws_data._meta.get_field("aws_key_id")
            key_object = aws_data._meta.get_field("aws_key")
            aws_key_id = key_id_object.value_from_object(obj)
            aws_key= key_object.value_from_object(obj)
            aws = platforms.aws.aws(aws_key_id, aws_key)
            for file in user_selection:
                if file == 'on':
                    print('False')
                else:
                    file_name = ast.literal_eval(file)
                    aws.download_image('testbucket1293248523850923853', file_name['name'])
                    json_acceptable_string = file.replace("'", "\"")
                    files_to_download.append(json.loads(json_acceptable_string))
            context['files'] = files_to_download
            return render(request, self.success_template, context)

        elif cloud == 'dropbox':
            for file in user_selection:
                if file == 'on':
                    print('False')
                else:
                    file_name = ast.literal_eval(file)
                    files_to_download.append(file_name)
            context['files'] = files_to_download
            dropbox.dropbox_download_selected_entries(context['files'])
            return render(request, self.success_template, context)

        elif cloud == 'google':
            for file in user_selection:
                if file == 'on':
                    print('False')
                else:
                    files_to_download.append(ast.literal_eval(file))
            context['files'] = files_to_download
            if cloud == 'google':
                google.GDriveDownloader_files_to_download = files_to_download
                google.GDriveDownloader__download_File()
            return render(request, self.success_template, context)

'''
For Admins:
    The following class was implemented per the standard of AWS. If the new platform does not support OAuth2.0
    then additional views will need to be created to allow the login parameters required by the platform.
'''

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
                return redirect("/cloud/files/")   
            except:
                messages.error(request, 'Amazon Web Services Key or Key ID is incorrect!')                 

        else:
            form = AWS_AuthForm()

        return render(request, self.template_name, {'form': form})

def index_redirect(request):
    return redirect('index/')

