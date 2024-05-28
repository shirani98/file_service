from django.db import models
from django.contrib.auth.models import User


class File(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=1024)
    created_at = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class DownloadLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.ForeignKey(File, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} downloaded {self.file.name} on {self.timestamp}"
