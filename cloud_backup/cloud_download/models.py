#!/usr/bin/env python3

""" models for cloud backup application
Application:    Cloud Backup
File:           /cloud_backup/cloud_download/models.py
Description:    Django models for database storage
Language:       Python 3.8 Django 2.2
Dev Env:        Linux x64

Authors:        Ryan Breitenfeldt
                Noah Farris
                Trevor Surface
                Kyle Thomas
Class:          CptS 421/423 Fall '19 Spring '20
University:    Washington State University Tri-Cities
"""

from django.db import models

__authors__ = ['Ryan Breitenfeldt', 'Noah Farris', 'Trevor Surface', 'Kyle Thomas']


class aws_data(models.Model):
    """aws_data class stores the authentication credentials for the AWS module"""
    aws_key_id = models.CharField(max_length=500)
    aws_key = models.CharField(max_length=500)