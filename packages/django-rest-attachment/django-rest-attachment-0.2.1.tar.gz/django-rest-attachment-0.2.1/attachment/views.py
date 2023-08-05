import os
from django.conf import settings
from django.http import JsonResponse
from .utils import stream_download
from .models import Attachment


# @login_required
def download(request, pk=None, use_key=True):
    try:
        obj = Attachment.objects.get(pk=pk)
    except Attachment.DoesNotExist:
        return JsonResponse({'error': 'File does not exist'}, status=404)

    if request.user.is_authenticated or (use_key and obj.download_key == request.GET.get('key', '')):
        file_dir = str(obj.file)
        file_path = os.path.join(settings.MEDIA_DIR, file_dir)
        file_name = obj.name or file_dir.split('/')[-1]
        return stream_download(file_path, file_name)
    else:
        return JsonResponse({'error': 'user not authenticated or key is incorrect'}, status=403)
