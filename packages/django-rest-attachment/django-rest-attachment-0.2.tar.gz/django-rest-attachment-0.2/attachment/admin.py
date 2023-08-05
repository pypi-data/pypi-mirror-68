from django.contrib import admin
from .base_admin import BaseAttachmentAdmin
from .models import Attachment


class AttachmentAdmin(BaseAttachmentAdmin):
    list_display = ('id', 'file', 'name', 'download_link', 'download_key')


admin.site.register(Attachment, AttachmentAdmin)
