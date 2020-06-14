import time
import logging
import datetime
from datetime import timedelta

from celery import shared_task
from celery.task.schedules import crontab
from celery.decorators import periodic_task, task

from django.utils import timezone
from django.core.cache import cache
from django.contrib.postgres.fields.jsonb import KeyTextTransform

from Graphize import settings

log = logging.getLogger(__name__)


@shared_task(name='file_optimizer', queue='default_queue')
def file_optimizer(uuid, **kwargs):
    '''
        - downscale image to width = 600px, height = 1200px
        - downscale video to 480p
        - leave lower resolution as it is
    '''

    from apps.grapher.models import Graphie
    from apps.grapher.models import FileManager
    from common.file_handler import delete_file_from_disk
    from common.file_handler import process_image_file
    from common.file_handler import process_video_file

    time.sleep(2)
    filemanager = FileManager.objects.get(uu=uuid)

    if filemanager.filetype == "1":
        filepath = f"{settings.MEDIA_ROOT}/images/{filemanager.data['filename']}"
        process_image_file(filemanager.data["temp_path"], filepath)
        delete_file_from_disk(filemanager.data["temp_path"])

    else:
        filepath = f"{settings.MEDIA_ROOT}/videos/{filemanager.data['filename']}"
        process_video_file(filemanager.data["temp_path"], filepath)
        delete_file_from_disk(filemanager.data["temp_path"])

    # store the path to processed file
    filemanager.filepath = '/media/' + filepath.split('/media/')[-1]
    filemanager.save()

    # mark the status of the file as processed
    graphie = Graphie.objects.get(illustration=filemanager)
    graphie.status='2'
    graphie.save()
