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
    from apps.grapher.models import FileManager

    filemanager = FileManager.objects.get(uu=uuid)

    filemanager.data["test"] = True
    filemanager.save()
