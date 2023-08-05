import os
from django.db import models
from django.conf import settings
from django.core.files.storage import FileSystemStorage


class MediaFileSystemStorage(FileSystemStorage):
    from django.conf import settings

    def __init__(self, location=settings.MEDIA_ROOT, base_url=settings.MEDIA_URL):
        super(MediaFileSystemStorage, self).__init__(location, base_url)

    # 重写 _save方法
    def _save(self, name, content):
        import hashlib
        import os

        # 文件扩展名
        ext = os.path.splitext(name)[1]
        # 文件目录
        d = os.path.dirname(name)
        # md5sum as file name
        md5 = hashlib.md5(content.read()).hexdigest()
        # rewrite directory
        d = os.path.join(d, md5[:1], md5[1:2])
        # rewrite filename
        fn = md5
        # rewrite file full path
        name = os.path.join(d, fn + ext)

        if self.exists(name):
            return name

        # 调用父类方法
        return super(MediaFileSystemStorage, self)._save(name, content)


class BaseAttachment(models.Model):
    # document = models.FileField('File', upload_to='documents/')
    file = models.FileField(
        'File', upload_to='files', storage=MediaFileSystemStorage())
    name = models.CharField(max_length=255, blank=True)
    url = models.URLField(max_length=200, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL,
                                    blank=True, null=True,
                                    on_delete=models.CASCADE, related_name='+')

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if self.name == "" or self.name is None:
            file_name = os.path.split(str(self.file))[1]
            self.name = file_name

        super().save(*args, **kwargs)
