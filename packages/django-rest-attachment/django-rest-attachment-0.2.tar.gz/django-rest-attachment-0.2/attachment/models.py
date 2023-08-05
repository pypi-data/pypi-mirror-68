from django.urls import reverse
from django.utils.crypto import get_random_string
from django.utils.html import format_html
from django.db import models
from django.contrib.auth.models import Group
from .base_models import BaseAttachment


class Attachment(BaseAttachment):
    owner_groups = models.ManyToManyField(Group, blank=True)
    download_key = models.CharField(max_length=16, default=get_random_string, editable=False)

    def download_link(self):
        url = reverse('attachment:download', args=[self.id])
        html = '<a href="{}">{}</a>'
        return format_html(html, url, self.name)
