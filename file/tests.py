from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User
from .views import FileDownloadView
from .models import File, DownloadLog
from rest_framework_simplejwt.tokens import AccessToken
import tempfile
from rest_framework.test import force_authenticate


class FileDownloadViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username="testuser", password="12345")
        self.access_token = AccessToken.for_user(self.user)
        self.tmp_file = tempfile.NamedTemporaryFile(delete=False)
        self.tmp_file.write(b"Test file content")
        self.tmp_file.close()
        self.file_name = self.tmp_file.name.split("/")[-1]
        self.file = File.objects.create(name=self.file_name, address=self.tmp_file.name)

    def test_download_view(self):
        request = self.factory.get(f"/api/files/download/{self.file_name}")
        force_authenticate(request, user=self.user)
        response = FileDownloadView.as_view()(request, file_name=self.file_name)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            DownloadLog.objects.filter(user=self.user, file=self.file).exists()
        )
        self.assertEqual(response.getvalue(), b"Test file content")

    def test_download_view_file_not_found(self):
        request = self.factory.get(f"/api/files/download/{self.file_name}")
        force_authenticate(request, user=self.user)
        response = FileDownloadView.as_view()(request, file_name="nonexistentfile.txt")
        self.assertEqual(response.status_code, 404)
