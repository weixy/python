from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=256, default=None)
    description = models.TextField(max_length=512, default=None)

    def __unicode__(self):
        return self.name


class Domain(models.Model):
    product = models.ForeignKey(Product)
    name = models.CharField(max_length=256, default=None)
    url = models.CharField(max_length=256, default=None)

    def __unicode__(self):
        return self.name