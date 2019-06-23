from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from .storage import ExternalStorage
from django.conf.global_settings import MEDIA_ROOT
from sorl.thumbnail import ImageField, get_thumbnail


from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys


MALE = 'ML'
FEMALE = 'FM'
OTHER = 'OC'
NOTANSWER = 'NA'

GENDER = (
    (MALE, 'ML'),
    (FEMALE, 'FM'),
    (OTHER, 'OC'),
    (NOTANSWER, 'NA'),
)

# Create your models here.
class Gallery(models.Model):
    GalleryOwner = models.ForeignKey(User, on_delete=models.CASCADE, default=1, null=True, blank=True)
    AlbumCover = models.ImageField(default='album_cover/default.jpeg', storage=ExternalStorage(),blank=True,null=True)
    Name = models.CharField(max_length=50, null=False, blank=False)
    Description = models.CharField(default='', null=True, blank=True, max_length=1024)
    UploadDateTime = models.DateTimeField(auto_now_add=True, null=True, editable=False)

    def __str__(self): return str(self.Name) + " - " + str(self.GalleryOwner) + "ID: " + str(self.id)

class GalleryReaction(models.Model):
    User = models.IntegerField(null=True, blank=True)
    Gallery = models.IntegerField(null=True, blank=True)
    UpdateDateTime = models.DateTimeField(auto_now_add=True, null=True, editable=False)

    def __str__(self): return str(User) + " - " + str(self.Gallery)

class Photo(models.Model):
    Gallery = models.IntegerField(null=True, blank=True)  #TODO is this corrent ?
    Photo = models.ImageField(default='photos/default.jpg',storage=ExternalStorage(),blank=True, null=True)
    UploadDateTime = models.DateTimeField(auto_now_add=True, null=True, editable=False)
    Location = models.CharField(default='', blank=True, null=True, max_length=50)   #INIT AS START.CHECK IF WE WANT LONGTITUDE, LATITUDE
    Description = models.CharField(default='', blank=True, null=True, max_length=1024)

    def __str__(self):
        return str(self.Gallery)

class PhotoReaction(models.Model):
    User = models.IntegerField(null=True, blank=True)
    Photo = models.IntegerField(null=True, blank=True)
    UpdateDateTime = models.DateTimeField(auto_now_add=True, null=True, editable=False)

    def __str__(self): return str(User) + " - " + str(self.Photo)

##TODO MAYBE ADD GALLERY OWNER
class GalleryComment(models.Model):
    User = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    Gallery = models.IntegerField(null=True, blank=True)
    UploadDateTime = models.DateTimeField(default=None, null=True, editable=False)
    Comment = models.CharField(max_length=1024, blank=True, null=True)
    #NOTIFICATIONS NOT ADDED

    def __str__(self): return str(self.Gallery) + " - " + str(self.UploadDateTime)

class PhotoComment(models.Model):
    User = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    Photo = models.IntegerField(null=True, blank=True)
    UpdateDateTime = models.DateTimeField(auto_now_add=True, null=True, editable=False)
    Comment = models.CharField(max_length=1024, blank=True, null=True)

    # NOTIFICATIONS NOT ADDED
    def __str__(self): return str(self.Photo) + " - " + str(self.Comment)

class Follow(models.Model): # authorize maybe?
    FollowCond1 = models.IntegerField(null=False, blank=False)
    FollowCond2 = models.IntegerField(null=False, blank=False)

    # Cond2 can view Cond1
    # Follower can view followed
    # NOTIFICATIONS NOT ADDED
    def __str__(self): return str(self.FollowCond2) + " can view content of " + str(self.FollowCond1) +" FollowID= " + str(self.id)

class Profile(models.Model):    # authorization demanded for sure
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    ProfilePhoto = models.ImageField(default='/profile_pics/default.jpg',storage=ExternalStorage(), null=True, blank=True)
    RegisterDateTime = models.DateTimeField(auto_now_add=True, null=True, editable=False)
    BirthDate = models.DateField(null=True, blank=True, editable=True)
    Bio = models.CharField(default='', max_length=500, blank=True, null=True)
    FirstName = models.CharField(default='', max_length=20, blank=True, null=False)
    LastName = models.CharField(default='', max_length=30, blank=True, null=False)
    Sex = models.CharField(default=NOTANSWER, null=False, blank=False, max_length=2, choices=GENDER)

    def __str__(self): return("User:" + str(self.user.username) + "Profile ID:" + str(self.id))    # this is what it is going to show