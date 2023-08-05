from django.contrib import admin
from django.utils.safestring import mark_safe


class BaseAttachmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'uploaded_at', 'uploaded_by', 'doc_tag')
    list_filter = ('uploaded_at', 'uploaded_by',)
    list_per_page = 20
    readonly_fields = ('doc_tag',)
    list_select_related = ('uploaded_by',)
    raw_id_fields = ('uploaded_by',)

    def doc_tag(self, obj):
        return mark_safe('<a href="{}" height="150">{}</a>'.format(obj.file.url, obj.name))

    doc_tag.short_description = u'Document'

    def save_model(self, request, obj, form, change):
        user = request.user
        instance = form.save(commit=False)
        if not change or not instance.owner:
            instance.uploaded_by = user
        instance.save()
        form.save_m2m()
        return instance
