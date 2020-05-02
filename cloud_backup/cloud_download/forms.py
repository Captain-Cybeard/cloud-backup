#!/usr/bin/env python3

""" forms for cloud backup application
Application:    Cloud Backup
File:           /cloud_backup/cloud_download/forms.py
Description:    Django forms for aws auth
Language:       Python 3.8 Django 2.2
Dev Env:        Linux x64

Authors:        Noah Farris
Class:          CptS 421/423 Fall '19 Spring '20
University:     Washington State University Tri-Cities
"""

from django import forms
from .models import aws_data
from . import platforms

__authors__ = 'Noah Farris'

class AWS_AuthForm(forms.ModelForm):
    """AWS_AuthForm is the django form to gather user AWS credentials."""
    aws_key_id = forms.CharField(widget=forms.TextInput(attrs={"onFocus":"field_focus(this, 'aws_key_id');", "onblur":"field_blur(this, 'aws_key_id')"}), label='Key Id', max_length=100)
    aws_key = forms.CharField(label='Key', max_length=100)

    class Meta:
        model = aws_data
        managed = False
        fields = ('aws_key_id', 'aws_key',)

    def clean_message(self):
        aws_key_id = self.cleaned_data.get('aws_key_id')
        aws_key = self.cleaned_data.get('aws_key')
        try:
            platforms.aws.aws(aws_key_id, aws_key).get_image_list()
        except:
            forms.ValidationError("Incorrect username or password")