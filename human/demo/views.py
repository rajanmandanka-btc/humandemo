from django.shortcuts import render

from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.viewsets import ModelViewSet
from .models import FileUpload
from .serializers import FileUploadSerializer
from subprocess import Popen, PIPE


# Create your views here.


class FileUploadViewSet(ModelViewSet):
    queryset = FileUpload.objects.all()
    serializer_class = FileUploadSerializer
    parser_classes = (MultiPartParser, FormParser,)

    def perform_create(self, serializer):
        print("data-----------------", )
        content_file = self.request.data.get('datafile')

        with open(content_file, "rb") as infile:
            p = Popen(["ffmpeg", "-i", "-", "-f", "matroska", "-vcodec", "mpeg4",
                       "-acodec", "aac", "-strict", "experimental", "-"],
                      stdin=infile, stdout=PIPE)
            while True:
                data = p.stdout.read(1024)
                if len(data) == 0:
                    break
                # do something with data...
                print(data)
                print("=============> ", "finished ------ ")
            p.wait()  # should have finisted anyway

        serializer.save(owner=self.request.user,
                        datafile=self.request.data.get('datafile'))
