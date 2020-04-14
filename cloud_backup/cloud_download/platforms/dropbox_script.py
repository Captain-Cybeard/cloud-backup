#!/bin/python
import dropbox
import json
from Api_keys import *

#####################################################################
# dropbox.oauth.DropboxOAuth2FlowNoRedirect(key, secret)
# dropbox.oauth.DropboxOAuth2FlowNoRedirect(key, secret).start()
# dropbox.oauth.DropboxOAuth2FlowNoRedirect(key, secret).finish(code)
# dropbox.dropbox.Dropbox(access_token)
# dropbox.dropbox.Dropbox(access_token).list_folder_result(path)
#   returns: dropbox.files.Metadata()
#       includes:   files.Metadata.name
#                   files.Metadata.path_lower 
#                   files.Metadata.path_display 
#                   files.Metadata.parent_shared_folder_id
#   raises: dropbox.exceptions.ApiError()
#       includes:   request_id
#                   error 
#                   user_message_text
# dropbox.dropbox.Dropbox(access_token).files_list_folder_continue(cursor)
#   retuns: dropbox.files.Metadata()
#   raises: dropbox.exceptions.ApiError()
#dropbox.dropbox.Dropbox(access_token).files_download_to_file(download_path, path)
#   returns: dropbox.files.FileMetadata()
#       includes:   files.FileMetadata.id
#                   files.FileMetadata.client_modified
#                   files.FileMetadata.server_modified 
#                   files.FileMetadata.rev 
#                   files.FileMetadata.size 
#                   files.FileMetadata.media_info 
#                   files.FileMetadata.symlink_info 
#                   files.FileMetadata.sharing_info 
#                   files.FileMetadata.is_downloadable 
#                   files.FileMetadata.export_info 
#                   files.FileMetadata.property_groups
#                   files.FileMetadata.has_explicit_shared_members  
#                   files.FileMetadata.content_hash
####################################################################


'''
POSSIBLY USEFUL FOR WEBSITE
from selenium import webdriver

options = webdriver.ChromeOptions() 
options.add_argument("download.default_directory=C:/Downloads")

driver = webdriver.Chrome(chrome_options=options)
'''

class DropBox(object):
    def __init__(self):
        self.dropbox_api_key = Dropbox_Api_key
        self.dropbox_api_secret = Dropbox_Api_secret
        self.dropbox_authentication_auth_flow = ""
        self.dropbox_authentication_authorize_url = ""
        self.dropbox_authentication_auth_code = ""
        self.dropbox_authentication_oauth_result = ""
        self.dbx = ""
        self.dropbox_get_files_return = ""
        self.dropbox_get_files_list_result = []
        self.dropbox_entries_to_download_list = []
        self.dropbox_download_path = "/mnt/c/Users/tsesu/Downloads/"
        self.dropbox_format_json = ""

    def dropbox_authentication(self):
        self.dropbox_authentication_auth_flow = dropbox.oauth.DropboxOAuth2FlowNoRedirect(self.dropbox_api_key, self.dropbox_api_secret)
        self.dropbox_authentication_authorize_url = self.dropbox_authentication_auth_flow.start()
        print("1. Go to: " + self.dropbox_authentication_authorize_url)
        print("2. Click \"Allow\" (you might have to log in first)")
        print("3. Copy the authorization code.")
        self.dropbox_authentication_auth_code = input("Enter the authorization code here: ").strip()

        try:
            self.dropbox_authentication_oauth_result = self.dropbox_authentication_auth_flow.finish(self.dropbox_authentication_auth_code)
        except Exception as e:
            print("Error: %s" % (e,))

        self.dbx = dropbox.dropbox.Dropbox(self.dropbox_authentication_oauth_result.access_token) #renaming for readability

    def dropbox_get_files_list(self):
        self.dropbox_get_files_list_return = self.dbx.files_list_folder("", recursive=True)
        for dropbox_files in self.dropbox_get_files_list_return.entries:
            self.dropbox_get_files_list_result.append(dropbox_files)
    
        return self.dropbox_get_files_list_result

    def dropbox_format_entries_list(self): #Test new function
        root_dict = {'path': '', 'dirs':[], 'files':[]}
        file_list = []
        for file_paths in self.dropbox_get_files_list_result:
            file_list.append(file_paths.path_lower)
        for file_path in file_list:
            if file_path.count('/') == 1:
                dict = {'path': file_path}
                if '.' in file_path:
                    dict['name'] = file_path.split('/')[len(file_path.split('/')) - 1]
                    if dict not in root_dict['files']:
                        root_dict['files'].append(dict)
                else:
                    dict['dirs'] = []
                    dict['files'] =[]
                    self.dropbox_format_entries_ruc(dict, 2, file_list)
                    if dict not in root_dict['dirs']:
                        root_dict['dirs'].append(dict) 
        root_json = json.dumps(root_dict)
        self.dropbox_format_json = root_json

    def dropbox_format_entries_ruc(self, build_dict, level, file_list):
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
                    self.dropbox_format_entries_ruc(dict, level + 1, file_list)
                    if dict not in build_dict['dirs']:
                        build_dict['dirs'].append(dict)         

    def dropbox_select_entries_to_download(self):
        number_string = raw_input("\nPlease select files to download by number: ")
        print("Selected Files:")
        for numbers in number_string:
            if(numbers != " "):
                self.dropbox_entries_to_download_list.append(self.dropbox_get_files_list_result[int(numbers)])
        for e in self.dropbox_entries_to_download_list:
            print(e.name)
'''
    def dropbox_download_selected_entries(self, list_of_selected_downloads=null, path):
        #this function will download the list of specified files to the path given by the user
'''

##Main
test = DropBox()
test.dropbox_authentication()

file_list = test.dropbox_get_files_list()

test.dropbox_format_entries_list()    
print(test.dropbox_format_json)
#test.select_entries_to_download()
# download_path = "/mnt/c/Users/tsesu/Downloads/"
# for numbers in number_string:
#     if(numbers != " "):
#         path = file_list[int(numbers)].path_lower
#         print(path)
# #dbx.files_download_to_file(download_path, path)