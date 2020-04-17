from django.shortcuts import render, redirect
from django.views import View


class Index(View):
    index_template = 'cloud_download/index.html'

    def get(self, request):
        print("get")  # DEBUGGING, remove later

        # Here the platforms needs to be dynamic list of the platforms, not sure how to do that yet
        context = {'platforms': ['google', 'dropbox', 'aws']}
        return render(request, self.index_template, context)

    def post(self, request):
        # Right now we just print out the user input (its the csrf token and the platform at the end
        # Here the redirect will point towards cloud authentication?
        print("post")  # DEBUGGING, remove later
        print(request.body)  # DEBUGGING, remove later
        return redirect('files/')


class Files(View):
    template = 'cloud_download/files.html'

    def get(self, request):
        context = {'files': ['/home', '/home/bart', '/root', 'hello.c']}
        return render(request, self.template, context)


def index_redirect(request):
    return redirect('index/')
