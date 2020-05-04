#!/usr/bin/env python3

''' Dropbox Platform
Application:     Cloud Backup
File:                 /cloud_backup/cloud_download/platforms/dropbox_script.py
Description:    Dropbox cloud platform
Language:       Python 3.8 Django 2.2
Dev Env:         Linux x64

Authors:          Trevor Surface
Class:              CptS 421/423 Fall '19 Spring '20
University:    Washington State University Tri-CIties
'''
import os
import dropbox
import json
from django.shortcuts import redirect
from . import Api_keys

__author__ = "Trevor Surface"

'''
dropbox.oauth.DropboxOAuth2Flow(key, secret, redirect_uri, session, token_type)
dropbox.oauth.DropboxOAuth2Flow(key, secret, redirect_uri, session, token_type).start()
    returns: redirect URL STR
dropbox.oauth.DropboxOAuth2Flow(key, secret, redirect_uri, session, token_type).finish(GET_parameters)
    returns: OAuth2FlowResult
    raises: dropbox.oauth.BadRequestException
            dropbox.oauth.BadStateException
            dropbox.oauth.CsrfException
            dropbox.oauth.NotApprovedException
            dropbox.oauth.ProviderException
dropbox.dropbox.Dropbox(access_token)
dropbox.dropbox.Dropbox(access_token).list_folder_result(path)
  returns: dropbox.files.Metadata()
      includes:   files.Metadata.name
                  files.Metadata.path_lower 
                  files.Metadata.path_display 
                  files.Metadata.parent_shared_folder_id
  raises: dropbox.exceptions.ApiError()
      includes:   request_id
                  error 
                  user_message_text
dropbox.dropbox.Dropbox(access_token).files_list_folder_continue(cursor)
  retuns: dropbox.files.Metadata()
  raises: dropbox.exceptions.ApiError()
dropbox.dropbox.Dropbox(access_token).files_download_to_file(download_path, path)
   returns: dropbox.files.FileMetadata()
       includes:   files.FileMetadata.id
                   files.FileMetadata.client_modified
                   files.FileMetadata.server_modified 
                   files.FileMetadata.rev 
                   files.FileMetadata.size 
                   files.FileMetadata.media_info 
                   files.FileMetadata.symlink_info 
                   files.FileMetadata.sharing_info 
                   files.FileMetadata.is_downloadable 
                   files.FileMetadata.export_info 
                   files.FileMetadata.property_groups
                   files.FileMetadata.has_explicit_shared_members  
                   files.FileMetadata.content_hash
dropbox.dropbox.Dropbox(access_token).files_download_zip_to_file(download_path, path)
    returns: dropbox.files.DownloadZipResult
    raises: dropbox.exceptions.ApiError()
        includes:   dropbox.files.DownloadZipError
'''

class DropBox(object):
    def __init__(self):
        '''
        __init__
        Attributes to modify:
        self.__dropbox_api_key, self.__dropbox_api_secret
            Admin needs to create an app via the dropbox app console: https://dropbox.com/developer
            Once the app has been created, Admin will get both a KEY and a SECRET, both of which 
            should be added to an API_Keys.py file, with parameter names Dropbox_Api_key and 
            Dropbox_Api_secret. Make sure to include the file in the .gitignore.
        self.__dropbox_download_path
            Admin needs to specify a location on the server that will store the downloaded files,
            additionally, for larger applications, the user may be asked to specify a location.
        '''
        self.dbx = None
        '''
            This attribute will contain the dropbox object after a users has been authenticated
        '''
        self.__dropbox_api_key = Api_keys.Dropbox_Api_key
        '''
        See __init__, Attributes to modify
        '''
        self.__dropbox_api_secret = Api_keys.Dropbox_Api_secret
        '''
        See __init__, Attributes to modify
        '''
        self.__dropbox_authentication_oauth_result = ""
        '''
            This attribute will contain the oath information, which includes the access token
            See the dropbox function definition at the top of the screen
        '''
        self.__dropbox_get_files_return = ""
        '''
            This attribute will contain the result returned by the dropbox.get_file_list_folder()
            api call, defined in the above api definitions
        '''
        self.__dropbox_get_files_list_result = []
        '''
            This attribute will contain a list of results with information from the previous attribute
            accessing the .entries parameter of the return
        '''
        self.__dropbox_download_path = os.environ['HOME'] + "/Downloads"
        '''
            See __init__, Attributes to modify
        '''
        self.dropbox_format_dict = {'path': '', 'dirs':[], 'files':[]}
        '''
            This attribute holds a dict for each folder, containing a variable list of folders in each level,
            and the included files within a given folder
        '''
        self.dropbox_flat_dict = {'files':[]}
        '''
            This attribute holds a flattened dict that will only show users files, not including the folders
            of the neccessary files. 
        '''
        self.__dropbox_files_paths = []
        '''
            This attribute stores the paths of the files returned from the dropbox.get_file_list_folder() 
        '''

    def dropbox_auth_flow(self, request):
        '''
            This function generates the flow object that needs to be passed through
            the authentication_start() method and the authentication_finish() method
        
        For Admin's:
            The redirect_uri parameter needs to be set in both the urls.py/urlpatterns as
            a path, which calls the dropbox_authetication_finish function. Additionally
            in the app console for dropbox (https://dropbox.com/developer) the same redirect_uri
            needs to be specified for the generated application. 
        '''
        redirect_uri = "http://localhost:8000/cloud/dropbox-auth-finish"
        return dropbox.oauth.DropboxOAuth2Flow(self.__dropbox_api_key, self.__dropbox_api_secret, redirect_uri, request, "dropbox-auth-csrf-token")

    def dropbox_authentication_start(self, web_app_session):
        '''
            This function generates the redirect for the application users to login to their 
            dropbox accounts
        '''
        authorize_url = self.dropbox_auth_flow(web_app_session.session).start()
        return redirect(authorize_url)

    def dropbox_authentication_finish(self, request):
        '''
            This function finalizes the authentication with the application user
            
        For Admins:
            The exceptions for Bad State, needs to be updated to the path that initialized the 
            authentication. This needs to be updated in the urls.py/urlpatterns, with a path that 
            calls the dropbox_authentication_start method.

            Additionally the Not Approved Exception return will need to be updated so that the application
            user is redirected to the home page of the webiste.
        '''
        try:
            self.__dropbox_authentication_oauth_result = self.dropbox_auth_flow(request.session).finish(request.GET)
        except dropbox.oauth.BadRequestException as e:
            raise e
        except dropbox.oauth.BadStateException as e:
            return redirect("http://localhost:8000/cloud/dropbox-auth-start/")
        except dropbox.oauth.CsrfException as e:
            return HttpResponseForbidden
        except dropbox.oauth.NotApprovedException as e:
            flash('Not approved?  Why not?')
            return redirect("http://localhost:8000/cloud")
        except dropbox.oauth.ProviderException as e:
            logger.log("Auth error: %s" % (e,))
            raise e
        self.dbx = dropbox.dropbox.Dropbox(self.__dropbox_authentication_oauth_result.access_token)
        ''' The above function call uses the oauth_return to generate the dropbox object'''
        self.dropbox_get_files_list()
        ''' The above function uses the dropbox api's to gather the list of folders and files the authenticated user
            has in their dropbox account, for further details see the function definition below'''
        self.dropbox_format_entries_recur(self.dropbox_format_dict, 1, self.__dropbox_files_paths)
        ''' The above funtion generates a dict, or json, depending upon the use of the #json.dumps comment in the 
            function defined below. The admin can change the views page to either display the json or dict'''
            #self.dropbox_format_dict = json.dumps(self.dropbox_format_dict)
        self.dropbox_dict_flatten_recur(self.dropbox_format_dict)
        ''' The above function flattens the dict to only show the files that are available on the application users 
            dropbox account, this can be removed if the Admin would like to show the directories WARNING: The application
            is only set up to show a flat_dict object, and will need further editing to enable the full dict view'''
        return redirect('/cloud/files') 
        ''' The final part of the function will redirect the user to the files view.py page, where their dropbox files will
            be displayed for them to choose which to download to the server'''

    def dropbox_get_files_list(self):
        '''
            This function calls the files_list_to_folder() dropbox function, gathering the list of application user dropbox
            files and folders. The application will then generate two lists in order to create a proper display for the user
            in the cloud/files/ view.
        '''
        try:
            self.__dropbox_get_files_list_return = self.dbx.files_list_folder("", recursive=True)
        except dropbox.exception.ApiError as e:
            raise e
        for dropbox_files in self.__dropbox_get_files_list_return.entries:
            self.__dropbox_get_files_list_result.append(dropbox_files)
            self.__dropbox_files_paths.append(dropbox_files.path_lower)         
    
    def dropbox_format_entries_recur(self, build_dict, level, file_list):
        '''
            This function is a recursive algorithm designed to create a multi layered dict that will hold the 
            root folder, and the subsequent folders that a application user may have available in their dropbox
            WARNING: For the Admins, the current functionaliry is based on the fact that a user does not use a '.' 
            in their directory names, however, if they do the generated dict will be invalid and not show the proper 
            files and folders, this would need to be changed to allow file/folder detection.
        '''
        for file_paths in file_list:
            if file_paths.count('/') == level and build_dict['path'] in file_paths:
                dict = {'path': file_paths}
                if '.' in file_paths:
                    dict['name'] = file_paths.split('/')[len(file_paths.split('/')) - 1]
                    if dict not in build_dict['files']:
                        build_dict['files'].append(dict)
                else:
                    dict['dirs'] = []
                    dict['files'] =[]
                    self.dropbox_format_entries_recur(dict, level + 1, file_list)
                    if dict not in build_dict['dirs']:
                        build_dict['dirs'].append(dict)         

    def dropbox_dict_flatten_recur(self, dir):
        '''
            This function uses a recursive algorithm to strip off directories from a application user's dropbox
            system, only displaying all of their current files. 
        '''
        for files in dir['files']:
            self.dropbox_flat_dict['files'].append(files)
        for dirs in dir['dirs']:
            self.dropbox_dict_flatten_recur(dirs)

    def dropbox_download_selected_entries(self, download_list):
        '''
            This function is called after an application user has selected the files they wish to download.
        
        For Admins:
            This function works off the premise that users do not put a '.' in their folder names, this is not always 
            the case, in which a change would need to be made to allow file/folder detection. Additionally when downloading
            the software will not detect if there is a currently named file in the system with same name as the chosen download 
            file. In which case the download will be overwritten by the new download. 
        '''
        for files in download_list:
            if '.' in files['path']:
                try: 
                    self.dbx.files_download_to_file(self.__dropbox_download_path + '/' + files['name'], files['path'])
                except dropbox.exceptions.ApiError as e:
                    raise e
            else:
                try: 
                    self.dbx.files_download_zip_to_file(self.__dropbox_download_path + '/' + files['name'], files['path'])
                except dropbox.exceptions.ApiError as e:
                    raise e