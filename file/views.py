from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponse, Http404
from .models import File, DownloadLog
from .serializers import FileSerializer
import os
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication


class FileListView(APIView):
    def get(self, request):
        files = File.objects.all()
        serializer = FileSerializer(files, many=True)
        return Response(serializer.data)


class FileDownloadView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request, file_name):
        try:
            file = File.objects.get(name=file_name)
            file_path = file.address
            if os.path.exists(file_path):
                DownloadLog.objects.create(user=request.user, file=file)

                with open(file_path, "rb") as f:
                    response = HttpResponse(
                        f.read(), content_type="application/octet-stream"
                    )
                    response[
                        "Content-Disposition"
                    ] = f'attachment; filename="{os.path.basename(file_path)}"'
                    return response
            else:
                raise Http404
        except File.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
