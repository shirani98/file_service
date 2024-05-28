from celery import shared_task
from .models import File
import os


@shared_task
def scan_filesystem():
    base_directory = "/home/mahdi/test_mehdi/"
    for dirpath, _, filenames in os.walk(base_directory):
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            file_address = os.path.abspath(file_path)
            file_name = filename
            File.objects.update_or_create(
                name=file_name,
                defaults={"address": file_address},
            )
