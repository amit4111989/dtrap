from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Profiles(models.Model):
    profile = models.CharField(max_length=30,unique=True)

class Disease(models.Model):
    disease = models.CharField(max_length=30,unique=True)

class Main(models.Model):
    common_locations = models.TextField(max_length=1000)
    common_nouns = models.TextField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    profiles = models.TextField(max_length=100)
    diseases = models.ForeignKey('Disease',on_delete=models.CASCADE)