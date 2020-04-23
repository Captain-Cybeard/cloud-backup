from django.shortcuts import render, redirect
from django.views import View
from . import platforms

class Index(View):
    index_template = 'cloud_download/index.html'

    # not sure if this is the best way to do this?
    # Will have to match if/else block in the post() method
    platforms = ['google', 'dropbox', 'aws']
    cloud = None  # the user selected cloud platform

    def get(self, request):
        context = {'platforms': self.platforms}
        return render(request, self.index_template, context)

    def post(self, request):
        platform = request.POST['platform']
        if platform == 'google':
            print(platform)  # DEBUGGING
            cloud = platforms.gDriveDownloader.GDriveDownloader()
        elif platform == 'dropbox':
            print(platform)  # DEBUGGING
            cloud = platforms.dropbox_script.DropBox()
            print(cloud)
        elif platform == 'aws':
            print(platform)  # DEBUGGING
        else:
            print("Unsupported platform")
            return redirect('index/')

        return redirect('files/')


class Files(View):
    template = 'cloud_download/files.html'

    def get(self, request):
        context = {'files': ['/home', '/home/bart', '/root', 'hello.c']}
        return render(request, self.template, context)


def index_redirect(request):
    return redirect('index/')
