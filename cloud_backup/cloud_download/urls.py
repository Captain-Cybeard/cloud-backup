from django.urls import path

from . import views

urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('files/', views.Files.as_view(), name='files'),
]