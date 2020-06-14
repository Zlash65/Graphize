import inspect

from django.dispatch import receiver
from django.db.models.signals import post_delete

from apps.grapher.models import FileManager, Graphie

from common.logger import tracelog
from common.file_handler import delete_file_from_disk

from Graphize.settings import BASE_DIR


@receiver(post_delete, sender=FileManager)
def post_delete_filemanager(sender, instance, **kwargs):
    ''' delete file for the instance '''
    try:
        delete_file_from_disk(f"{BASE_DIR}/{instance.filepath}")
    except Exception as e:
        pass


@receiver(post_delete, sender=Graphie)
def post_delete_graphie(sender, instance, **kwargs):
    ''' delete file for the instance '''
    try:
        FileManager.objects.filter(id=instance.illustration.id).delete()
    except Exception as e:
        pass
