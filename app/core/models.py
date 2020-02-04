from django.db import models


class Client(models.Model):
    """Client data model."""
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255, blank=True)
    contact = models.CharField(max_length=25)

    def __str__(self):
        return self.name


class Staff(models.Model):
    """Staff data model."""
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255, blank=True)
    contact = models.CharField(max_length=25)
    NIP = models.CharField(max_length=16)

    def __str__(self):
        return self.name
