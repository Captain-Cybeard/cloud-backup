from __future__ import print_function
import pickle
import os.path
import io
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import flask
import google.oauth2.credentials
import google_auth_oauthlib.flow

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

    #https://developers.google.com/identity/protocols/oauth2/web-server
    def GDriveDownloader_redirect_authentication(self):
        auth_flask = flask()
        flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file('client_secret_204730000731-c0gs1os80ucalj6mto9c1etmaee70is7.apps.googleusercontent.com.json', self.GDriveDownloader_SCOPES)
        flow.redirect_uri = 'https://www.google.com'
        authorization_url, state = flow.authorization_url(access_type='offline',include_granted_scopes='true')
        auth_flask.redirect(authorization_url)
        auth_flask.session['state'] = state
        flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file('client_secret_204730000731-c0gs1os80ucalj6mto9c1etmaee70is7.apps.googleusercontent.com.json',scopes=self.GDriveDownloader_SCOPES,state=state)
        flow.redirect_uri = flask.url_for('https://www.google.com', _external=True)
        authorization_response = auth_flask.request.url
        flow.fetch_token(authorization_response=authorization_response)
        self.GDriveDownloader_creds = flow.credentials
        auth_flask.session['credentials'] = {
            'token': self.GDriveDownloader_creds.token,
            'refresh_token': self.GDriveDownloader_creds.refresh_token,
            'token_uri': self.GDriveDownloader_creds.token_uri,
            'client_id': self.GDriveDownloader_creds.client_id,
            'client_secret': self.GDriveDownloader_creds.client_secret,
            'scopes': self.GDriveDownloader_creds.scopes}


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
            #self.GDriveDownloader_file_List = self.GDriveDownloader_service.files().list(spaces='drive', fields='nextPageToken, items(id, title)', pageToken=page_token).execute()
            self.GDriveDownloader_file_List = self.GDriveDownloader_service.files().list(q="mimeType != 'application/vnd.google-apps.document' and mimeType != 'application/vnd.google-apps.spreadsheet' and mimeType != 'application/vnd.google-apps.presentation'",spaces='drive', fields='*' , pageToken=page_token).execute()
            for file in self.GDriveDownloader_file_List["files"]:
                # Process change
                #print 'Found file: %s (%s)' % (file.get('title'), file.get('id'))
                print(file["name"])
                print(file["id"])
                print()
                self.GDriveDownloader_json['files'].append({"name": file["name"],"id": file["id"]})
            page_token = self.GDriveDownloader_file_List.get('nextPageToken', None)
            if page_token is None:
                break


# takes dictionary as input in this formate: {"name": "file name", "id": " file id"}
    def GDriveDownloader_add_file_to_download(self,fileId):
        self.GDriveDownloader_files_to_download.append(fileId)


