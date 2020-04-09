from django.shortcuts import render

from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.viewsets import ModelViewSet
from .models import FileUpload
from .serializers import FileUploadSerializer
import ffmpeg


# Create your views here.


class FileUploadViewSet(ModelViewSet):
    queryset = FileUpload.objects.all()
    serializer_class = FileUploadSerializer
    parser_classes = (MultiPartParser, FormParser,)

    def perform_create(self, serializer):
        print("data-----------------", )
        content_file = self.request.data.get('datafile')
        print(content_file)

        try:
            (ffmpeg.input('test.mp4')
             .filter('fps', fps=2)
             .output('test/%d.png',
                     video_bitrate='5000k',
                     s='64x64',
                     sws_flags='bilinear',
                     start_number=0)
             .run(capture_stdout=True, capture_stderr=True))
        except ffmpeg.Error as e:
            print('stdout:', e.stdout.decode('utf8'))
            print('stderr:', e.stderr.decode('utf8'))

        # with open(content_file, "rb") as infile:
        #     p = Popen(["ffmpeg", "-i", "-", "-f", "matroska", "-vcodec", "mpeg4",
        #                "-acodec", "aac", "-strict", "experimental", "-"],
        #               stdin=infile, stdout=PIPE)
        #     while True:
        #         data = p.stdout.read(1024)
        #         if len(data) == 0:
        #             break
        #         # do something with data...
        #         print(data)
        #         print("=============> ", "finished ------ ")
        #     p.wait()  # should have finisted anyway

        serializer.save(datafile=self.request.data.get('datafile'))
