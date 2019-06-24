from django.db import models
from webmain.storage import ExternalStorage
from django.core.files.storage import *
from django.db.models.signals import post_delete
from django.dispatch import receiver

# Create your models here.
class Post(models.Model):
    title = models.TextField()
    cover = models.ImageField(upload_to='images/',storage=ExternalStorage())

    def __str__(self):
        return self.title

@receiver(post_delete, sender=Post)
def submission_delete(sender, instance, **kwargs):
    instance.cover.delete(False)