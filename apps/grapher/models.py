import uuid as uuid

from django.contrib.gis.db import models
from django.contrib.gis.geos import Point
from django.contrib.postgres.fields import JSONField

from common.logger import tracelog

TYPE = (('1', 'Image'),
        ('2', 'Video'),)


class Grapher(models.Model):
    '''
        - maintain Grapher (User) info separately
    '''
    uu = models.UUIDField(default=uuid.uuid4, unique=True)

    name = models.CharField(max_length=100)
    username = models.CharField(max_length=100, unique=True)

    created_at = models.DateTimeField(auto_now_add =True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return str(self.username)

    @staticmethod
    def add_grapher(data):
        '''
            - store grapher name  and username
            - if username not provided, use hash of name
            - if username already present, return the same
        '''
        from common.file_handler import get_content_hash

        name = data["grapher_name"]
        username = data.get("username", get_content_hash(name))
        try:
            grapher = Grapher.objects.create(name=name, username=username)
        except Exception as e:
            grapher = Grapher.objects.get(username=username)

        return grapher


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

    data = JSONField(default=dict, null=True, blank=True)
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
    grapher = models.ForeignKey(Grapher, related_name="grapher", on_delete=models.CASCADE)

    subject = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)
    location = models.PointField(geography=True, default=Point(0.0, 0.0))
    illustration = models.ForeignKey(FileManager, related_name="illustration", \
        null=True, blank=True, on_delete=models.CASCADE)

    data = JSONField(default=dict, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add =True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.subject)

    @staticmethod
    def add_graphie(data):
        '''
            - store grapher info or fetch if already exists
            - store story information
        '''
        try:
            grapher = Grapher.add_grapher(data)
            subject = data["subject"]
            description = data["description"]

            latitude, longitude = data.get("latitide", 0), data.get("longitude", 0)
            extra_data = {"latitude": latitude, "longitude": longitude}

            graphie = Graphie.objects.create(grapher=grapher, subject=subject, data=extra_data, \
                description=description, location=Point(latitude, longitude))

            return True, graphie

        except Exception as e:
            tracelog("ERROR SAVING GRAPHIE", repr(e))
            return False, None
