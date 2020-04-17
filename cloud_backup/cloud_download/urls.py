from django.urls import path

from . import views

urlpatterns = [
    path('', views.index_redirect),
    path('index/', views.Index.as_view(), name='index'),
    path('files/', views.Files.as_view(), name='files'),
]