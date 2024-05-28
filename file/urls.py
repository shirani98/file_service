from django.urls import path
from .views import FileListView, FileDownloadView

urlpatterns = [
    path(
        "download/<str:file_name>/",
        FileDownloadView.as_view(),
        name="file_download",
    ),
    path("", FileListView.as_view(), name="file_list"),
]
