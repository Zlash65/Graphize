import uuid as uuid
from decimal import Decimal

from django.contrib.gis.db import models
from django.contrib.gis.geos import Point
from django.contrib.postgres.fields import JSONField

from common.logger import tracelog

from Graphize.settings import TEMP_IMAGE_PATH
from Graphize.settings import TEMP_VIDEO_PATH

TYPE = (('1', 'Image'),
        ('2', 'Video'),)

PROCESSING  = (('1', 'Processing'),
                ('2', 'Completed'),)


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

    filesize = models.BigIntegerField(default=0)
    extension = models.CharField(max_length=20)  # eg. excel, pdf, img
    filename = models.CharField(max_length=100, null=True, blank=True)
    description = models.CharField(max_length=500, null=True, blank=True)
    content_hash = models.CharField(max_length=100, null=True, blank=True)
    filetype = models.CharField(max_length=2, choices=TYPE, null=True, blank=True)
    filepath = models.CharField(max_length=200, null=True, blank=True)

    data = JSONField(default=dict, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add =True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.filename)

    @staticmethod
    def add_file(data, graphie=None, file_content=None):
        '''
            - store the uploaded file at a temporary location
            - enqueue a task for downscaling
            - store other meta data and return status
        '''
        from apps.grapher.tasks import file_optimizer
        from common.file_handler import get_content_hash
        from common.file_handler import get_size_of_file

        try:
            # read file if file_content not given
            if not file_content:
                file_content = data["graphie"].read()

            # # if same file has been uploaded already, bypass processing
            content_hash = get_content_hash(file_content)
            # exists = FileManager.objects.filter(content_hash=content_hash).last()
            # if exists:
            #     graphie.illustration = exists
            #     graphie.save()
            #     return True

            # if file does not exist, store the metadata and queue for downscaling
            filetype = data["file_type"]
            extension = data["file_extension"]
            filename = data["graphie"].name.replace(data["graphie"].name.split('.')[-1], extension)

            file_path = f"{TEMP_IMAGE_PATH}/{graphie.uu}.{extension}" if filetype == "1" \
                else f"{TEMP_VIDEO_PATH}/{graphie.uu}.{extension}"

            with open(file_path, 'wb') as file_writer:
                file_writer.write(file_content)
            filesize = get_size_of_file(file_path)

            data = {"filename": f"{graphie.uu}.{extension}"}
            data.update({"temp_path": file_path})
            filemanager = FileManager.objects.create(filename=filename, filesize=filesize, \
                filetype=filetype, extension=extension,  content_hash=content_hash, data=data)

            graphie.illustration = filemanager
            graphie.save()

            file_optimizer.delay(filemanager.uu)
            return True

        except Exception as e:
            tracelog("FILE SAVING ERROR", repr(e))
            return False


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
    status = models.CharField(max_length=2, choices=PROCESSING, default='1')

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

            latitude = Decimal(data.get("latitude", 0))
            longitude = Decimal(data.get("longitude", 0))
            extra_data = {"latitude": str(latitude), "longitude": str(longitude)}

            graphie = Graphie.objects.create(grapher=grapher, subject=subject, data=extra_data, \
                description=description, location=Point([latitude, longitude]))

            return True, graphie

        except Exception as e:
            tracelog("ERROR SAVING GRAPHIE", repr(e))
            return False, None
