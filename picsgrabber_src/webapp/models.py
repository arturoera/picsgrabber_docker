from django.db import models


class Grabber(models.Model):
    image_id = models.CharField(max_length=50, default='', null=True, blank=True)
    description = models.CharField(max_length=10000, default='', null=True, blank=True)
    url = models.CharField(max_length=1000, default='', null=True, blank=True)
    downloaded = models.CharField(max_length=10, default='', null=True, blank=True)
    time_added = models.CharField(max_length=100, default='', null=True, blank=True)
