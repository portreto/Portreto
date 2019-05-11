from django.db import models

from django.utils.deconstruct import deconstructible
from django.template.defaultfilters import filesizeformat
from django.core.exceptions import ValidationError




# Create your models here.
class File(models.Model):
    file = models.FileField(blank=False, null=False)
    def delete(self):
        self.file.delete()
        super(File, self).delete()

    def __str__(self):
        return self.file.name