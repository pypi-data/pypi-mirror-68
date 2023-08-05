import os
from rest_framework import viewsets, mixins
from .models import Attachment
from .serializers import AttachmentSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from django.conf import settings

from .utils import stream_download


class AttachmentViewSet(mixins.CreateModelMixin, mixins.RetrieveModelMixin, mixins.ListModelMixin,
                        mixins.DestroyModelMixin,
                        viewsets.GenericViewSet):
    queryset = Attachment.objects.all()
    serializer_class = AttachmentSerializer
    permission_classes = [IsAuthenticated]

    # def get_list_queryset(self, request):
    #     qif = request.GET.get('qif')
    #     location = request.GET.get('location')
    #     loc_choices = enums.get_choice_list(enums.LOCATION_CHOICES)
    #     if qif:
    #         queryset = self.queryset.filter(qif=qif)
    #     else:
    #         raise ValidationError({'message': 'missing qif id'}, 400)
    #     if location in loc_choices:
    #         queryset = queryset.filter(location=location)
    #     return queryset

    def perform_create(self, serializer):
        serializer.save(uploaded_by=self.request.user)

    @action(methods=['get'], detail=True, permission_classes=[], name='download')
    def download(self, request, pk=None, use_key=True):
        obj = self.get_object()
        if request.user.is_authenticated or (
                use_key and obj.download_key == request.query_params.get('key', '')):
            file_dir = str(obj.file)
            file_path = os.path.join(settings.MEDIA_DIR, file_dir)
            file_name = obj.name or file_dir.split('/')[-1]
            return stream_download(file_path, file_name)
        else:
            return Response({'error': 'user not authenticated or key is incorrect'}, status=403)
