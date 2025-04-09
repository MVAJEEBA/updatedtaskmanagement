from django.shortcuts import render

# Create your views here.
from django.shortcuts import render

# Create your views here.
from django.contrib.auth.decorators import permission_required
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import TemplateView



@permission_required('myapp.can_publish_document', raise_exception=True)
def publish_document(request):
    return HttpResponse("You have permission to publish documents.")



class PublishDocumentView(PermissionRequiredMixin, TemplateView):
    template_name = 'publish.html'
    permission_required = 'myapp.can_publish_document'
