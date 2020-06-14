import uuid as uuid

from django.contrib.gis.db import models
from django.contrib.gis.geos import Point

from common.logger import tracelog

TYPE = (('1', 'Image'),
        ('2', 'Video'),)


class Grapher(models.Model):
    '''
        - maintain Grapher (User) info separately
    '''
    uu = models.UUIDField(default=uuid.uuid4, unique=True)

    name = models.CharField(max_length=100)
    username = models.CharField(max_length=100)

    created_at = models.DateTimeField(auto_now_add =True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return str(self.username)


class FileManager(models.Model):
    """
        - keep illustration of Graphie separate
    """

    uu = models.UUIDField(default=uuid.uuid4, unique=True)

    file_size = models.BigIntegerField(default=0)
    extension = models.CharField(max_length=20)  # eg. excel, pdf, img
    filename = models.CharField(max_length=100, null=True, blank=True)
    description = models.CharField(max_length=500, null=True, blank=True)
    content_hash = models.CharField(max_length=100, null=True, blank=True)
    type = models.CharField(max_length=2, choices=TYPE, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add =True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.filename)


class Graphie(models.Model):
    '''
        - maintain story here
        - each story is linked to one grapher
        - each story is linked to one form of image/video illustration
    '''

    uu = models.UUIDField(default=uuid.uuid4, unique=True)
    grapher = models.OneToOneField(Grapher, related_name="grapher", on_delete=models.CASCADE)

    subject = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)
    location = models.PointField(geography=True, default=Point(0.0, 0.0))
    illustration = models.OneToOneField(FileManager, related_name="illustration", on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add =True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.subject)
