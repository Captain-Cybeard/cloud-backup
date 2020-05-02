'''
For Admins:
    This Template class is to help developers add additional cloud platforms to the software
'''

'''
class [Platform_NAME](object):
    def __init__(self):
        ## For attributes use convention [NAME]_[FUNCTION]_[PARAM]
        ## The below attributes are strongly recomended to have within new platform classes  
        __[Platform_NAME]__user_download_path       #Consider this to be a private function
        __[Platform_NAME]_get_files_list_result     #Conisder this to be a private function
        __[Platform_NAME]_entries_to_download_list  #Consider this to be a private function
        [Platform_NAME]_format_dict
        [Platform_NAME]_flat_dict

    ##  For Admins - the following three functions are designed based off of the OAuth2 requriements
    ##  If the platform that is being added does not have OAuth2 authentication the following three functions 
    ##  are unneccessay.

    def [Platform_NAME]_authentication_flow(self, request):
        # This function call requires a redirect_uri that may need to need to be specified within the app console 
        # of the platform being used. This class should return the Flow component of the OAuth2 authentication. This 
        # will likey need a request.session to help manage state. 

    def [Platform_NAMe]_authentication_start(self):
        # This function will initiate the starting parameters for the OAuth2 authentication to use this 
        # capability appropriately, after this method is created, this object will need to be instatiated
        # within the veiws.py script. Additionally the urls.py/urlpattern needs to be updated with the following:
            path('[Platform_NAME]-auth-start', views.[Platform_NAME].[Platform_NAME]_authentication_start)
        # When the user selects the new plaform, the Views Index class will need to return a redirect function
        # redirect('[Platform_NAME]-auth-start')
        # Finally this method should instatiate a redirect_url to created by the authentication_flow method noted previously
        # The return will need a django.shortcuts.redirect() to the redirect_url to allow the user to log into the new platform

    def [Platform_NAME]_authentication_finish(self):
        # This fucntion will finalize the OAuth2 authentication. After this method is created, this object will need to be instatiated
        # within the veiws.py script. Additionally the urls.py/urlpattern needs to be updated with the following:
            path('[Platform_NAME]-auth-finish', views.[Platform_NAME].[Platform_NAME]_authentication_finish)
        # The authentication_flow, may require a redirect_uri that includes the full uri to the [Platform_NAME]-auth-finish
        # This function will catch any errors that arise within the OAuth2 authentication flow. 
        # This function will also call all neccessary function to gather files and folders of the application users platform.
        # The returned object will then need to be formated into either a dict specified as:
            {'path':'', 'dirs':[], 'files':[]} in which every dir contains the same dict and dict list for subsequent directories
        # Currently the software requires a flat_dict, in which all files are pulled out along with their full path and any required 
        # attributes neccessary for downloading. The flact dict will be written as
            {'file':[]} with all the attributes required for downloading files.

    def [Platform_NAME]_get_files_list(self):
        # This is a generic template for gathering files, use selected platforms api to gather the application users files and folders
        # Often this may have a list of file entires as a return

    def [Platform_NAME]_format_entries_list(self):
        # This function will take the return of [NAME]_get_files_list
        # And provide the neccessary information to pass to the views context to display the application users platform files
    
    def [Platform_NAME]_download_selected_entries(self, path):
        # This function will download the list returned by [NAME]_select_entries_to_download
        # Using the [NAME]_download_path to specify the location on the server where the files and folders will be uploaded to, 
        # This function should also include a warning that if a file is alread known on a system, it will not overwrite the file.
'''