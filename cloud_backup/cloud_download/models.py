from django.db import models

class aws_data(models.Model):
    aws_key_id = models.CharField(max_length=500)
    aws_key = models.CharField(max_length=500)