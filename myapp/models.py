from django.db import models
from django.db import models
from django.contrib.auth.models import User
from taskapp.models import *
from django.conf import settings
class Document(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    class Meta:
        permissions = [
            ("can_publish_document", "Can publish documents"),
            ("can_archive_document", "Can archive documents"),
        ]
    def __str__(self):
        return self.title


