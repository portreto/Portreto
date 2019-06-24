from django.contrib import admin
from .models import Gallery, GalleryReaction, Photo, PhotoReaction, GalleryComment, PhotoComment, Follow, Profile

# Register your models here.


admin.site.register([Gallery, GalleryReaction, Photo, PhotoReaction, GalleryComment, PhotoComment,
                     Follow, Profile])