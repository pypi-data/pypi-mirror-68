from rest_framework import serializers
from .models import Attachment


class AttachmentSerializer(serializers.ModelSerializer):
    uploader_id = serializers.ReadOnlyField(source='uploader.id')
    uploader = serializers.CharField(source='uploader.username', read_only=True)

    def save(self, **kwargs):
        user = self.context['request'].user
        user_docs = Attachment.objects.all().values_list('name', flat=True)
        file = str(self.validated_data['file'])
        name, ext = file.split('.')
        i, name = 1, name
        while file in user_docs:
            # file = f'{name} ({i}).{ext}'
            file = '{} ({}).{}'.format(name, i, ext)
            i += 1

        self.validated_data['name'] = file
        super().save(**kwargs)

    class Meta:
        model = Attachment
        fields = '__all__'
