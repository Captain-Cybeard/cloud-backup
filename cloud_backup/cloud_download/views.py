from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpResponseNotFound


class Index(View):
    template = 'index.html'

    def get(self, request):
        if request.method == 'POST':
            print("post")
            print(request.body)
        elif request.method == 'GET':
            print("get")
            context = {'platforms': ['google', 'dropbox', 'aws']}
            return render(request, self.template, context)
        else:
            print("404")
            return HttpResponseNotFound('404')

class Files(View):
    template = 'files.html'

    def get(self, request):
        context = {'files': ['/home', '/home/bart', '/root', 'hello.c']}
        return render(request, self.template, context)


def index_redirect(request):
    return redirect('index/')
