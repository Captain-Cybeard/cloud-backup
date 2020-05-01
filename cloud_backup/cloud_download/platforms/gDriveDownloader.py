#!/usr/bin/env python3

""" Google Drive Cloud Platform

Application:     Cloud Backup
File:                 /cloud_backup/cloud_download/platforms/gDriveDownloader.py
Description:    Google Drive Cloud Platform
Language:       Python 3.8 Django 2.2
Dev Env:         Linux x64

Authors:          Ryan Breitenfeldt
Class:              CptS 421/423 Fall '19 Spring '20
University:    Washington State University Tri-CIties
"""

from __future__ import print_function
import pickle
import os.path
import io
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from google_auth_oauthlib.flow import InstalledAppFlow
from google_auth_oauthlib.flow import Flow
from google.auth.transport.requests import Request
import google.oauth2.credentials
from google.oauth2.credentials import Credentials
from django.shortcuts import render, redirect

__author__ = 'Ryan Breitenfeldt'

#googleapiclient.discovery.build
#googleapiclient.discovery.build.files().list()
#googleapiclient.http.MediaIoBaseDownload
#google_auth_oauthlib.flow.InstalledAppFlow
#google.auth.transport.requests.Request


class GDriveDownloader():
    def __init__(self,creds=None,service=None):
        self.GDriveDownloader_creds = creds
        self.GDriveDownloader_SCOPES = ['https://www.googleapis.com/auth/drive']
        self.GDriveDownloader_service = service
        self.GDriveDownloader_file_List = None
        self.GDriveDownloader_json = {'files':[]}
        self.GDriveDownloader_files_to_download = []

    def GDriveDownloader_authentication(self):
        # If there are no (valid) credentials available, let the user log in.
        if not self.GDriveDownloader_creds or not self.GDriveDownloader_creds.valid:
            if self.GDriveDownloader_creds and self.GDriveDownloader_creds.expired and self.GDriveDownloader_creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file('client_secret_204730000731-c0gs1os80ucalj6mto9c1etmaee70is7.apps.googleusercontent.com.json', self.GDriveDownloader_SCOPES)
                self.GDriveDownloader_creds = flow.run_local_server(port=0)

    def GDriveDownloader_save_Token(self):
        with open('token.pickle', 'wb') as token:
            pickle.dump(self.GDriveDownloader_creds, token)

    def GDriveDownloader_load_Token(self):
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)

    def GDriveDownloader_build_Service(self):
        self.GDriveDownloader_service = build('drive', 'v3', credentials=self.GDriveDownloader_creds)

    def GDriveDownloader__download_File(self):
        for file_id in self.GDriveDownloader_files_to_download:
            request = self.GDriveDownloader_service.files().get_media(fileId=file_id["id"])
            fh = io.BytesIO()
            downloader = MediaIoBaseDownload(fh, request)
            done = False
            while done is False:
                status, done = downloader.next_chunk()
                print("Download {}%".format(int(status.progress() * 100)))
            f = open(file_id["name"], 'wb')
            f.write(fh.getvalue())

    def GDriveDownloader_get_Files(self):
        page_token = None 
        while True:
            self.GDriveDownloader_file_List = self.GDriveDownloader_service.files().list(q="mimeType != 'application/vnd.google-apps.document' and mimeType != 'application/vnd.google-apps.spreadsheet' and mimeType != 'application/vnd.google-apps.presentation' and mimeType != 'application/vnd.google-apps.folder'" ,spaces='drive', fields='*' , pageToken=page_token).execute()
            for file in self.GDriveDownloader_file_List["files"]:
                self.GDriveDownloader_json['files'].append({"name": file["name"],"id": file["id"]})
            page_token = self.GDriveDownloader_file_List.get('nextPageToken', None)
            if page_token is None:
                break


# takes dictionary as input in this formate: {"name": "file name", "id": " file id"}
    def GDriveDownloader_add_file_to_download(self,fileId):
        self.GDriveDownloader_files_to_download.append(fileId)

    def GDriveDownloaded_authentication_flow(self):    
        redirect_uri = "http://localhost:8000/cloud/google-auth-finish/"
        return Flow.from_client_secrets_file(
            'client_secret_204730000731-c0gs1os80ucalj6mto9c1etmaee70is7.apps.googleusercontent.com.json',
            scopes=self.GDriveDownloader_SCOPES,
            redirect_uri=redirect_uri)

    def GDriveDownloaded_authentication_start(self, request):    
        auth_uri = self.GDriveDownloaded_authentication_flow().authorization_url()[0]
        return redirect(auth_uri[:-20])

    def GDriveDownloaded_authentication_finish(self, request):    
        try:
            self.GDriveDownloader_creds = self.GDriveDownloaded_authentication_flow().fetch_token(code=request.GET['code'], state= request.GET['state'])
            #print(self.GDriveDownloader_creds)
            self.GDriveDownloader_creds = Credentials(self.GDriveDownloader_creds['access_token'])
            self.GDriveDownloader_build_Service()
            self.GDriveDownloader_get_Files()
        except Exception as e:
            raise e
        return redirect('/cloud/files')

