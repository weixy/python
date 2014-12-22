from django.db import models


class Scenario(models.Model):
    name = models.CharField(max_length=256)
    domain = models.CharField(max_length=256)


class LoadRequest(models.Model):
    scenario = models.ForeignKey(Scenario)
    url = models.CharField(max_length=256, default='/')
    type = models.CharField(max_length=10, default='GET')
    data = models.CharField(max_length=256, default=None)
    header = models.CharField(max_length=256, default=None)
    redirects = models.BooleanField(default=False)
