from django.contrib import admin

from .models import Document


class DocumentAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.groups.filter(name='Editor').exists():
            return qs.filter(created_by=request.user)
        return qs
admin.site.register(Document, DocumentAdmin)

class DocumentAdmin(admin.ModelAdmin):
    def get_fields(self, request, obj=None):
        fields = super().get_fields(request, obj)
        if not request.user.groups.filter(name='Admin').exists():
            fields.remove('created_by')
        return fields
