from django.contrib import admin
from .models import File, DownloadLog


admin.site.register(File)
admin.site.register(DownloadLog)