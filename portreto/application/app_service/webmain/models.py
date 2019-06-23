"""
    SK Edit
"""

from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from .storage import ExternalStorage

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

# Application Models

class Gallery(models.Model):
    GalleryOwner = models.ForeignKey(User, on_delete=models.CASCADE, default=None, null=True, blank=True)
    AlbumCover = models.ImageField(storage=ExternalStorage())
    Name = models.CharField(max_length=50, null=False, blank=False)
    Description = models.CharField(default='', null=True, blank=True, max_length=1024)
    UploadDateTime = models.DateTimeField(auto_now_add=True, null=True, editable=False)

    # def save(self, *args, **kwargs):
    #     super(Gallery, self).save(*args, **kwargs)
    #     pf = Image.open(self.AlbumCover.path)
    #
    #
    #     if pf.height > 800 or pf.width > 800:   # overwriting existing images in specific size
    #         output_size = (800, 800)
    #         pf.thumbnail(output_size)
    #         pf.save(self.AlbumCover.path)

    def __str__(self): return str(self.Name) + " - " + str(self.GalleryOwner)

class GalleryReaction(models.Model):
    User = models.ForeignKey(User, on_delete=models.CASCADE, default=1) #CHECK WITH DEFAULT.USER MUST CHANGE EVERY TIME
    Gallery = models.ForeignKey(Gallery, on_delete=models.CASCADE, default=1)
    UpdateDateTime = models.DateTimeField(auto_now_add=True, null=True, editable=False)

    def __str__(self): return str(User) + " - " + str(self.Gallery)

class Photo(models.Model):
    Gallery = models.ForeignKey(Gallery, on_delete=models.CASCADE, default=1)  #REMINDER. CAN A PHOTO BE BLANK?
    Photo = models.ImageField( storage=ExternalStorage())
    UploadDateTime = models.DateTimeField(auto_now_add=True, null=True, editable=False)
    Location = models.CharField(default='', blank=True, null=True, max_length=50)   #INIT AS START.CHECK IF WE WANT LONGTITUDE, LATITUDE
    Description = models.CharField(default='', blank=True, null=True, max_length=1024)

    def __str__(self):
        return str(self.Gallery)

class PhotoReaction(models.Model):
    User = models.ForeignKey(User, on_delete=models.CASCADE, default=1) #CHECK WITH DEFAULT.USER MUST CHANGE EVERY TIME
    Photo = models.ForeignKey(Photo, on_delete=models.CASCADE, default=1)
    UpdateDateTime = models.DateTimeField(auto_now_add=True, null=True, editable=False)

    def __str__(self): return str(User) + " likes " + str(self.Photo)

class GalleryComment(models.Model):
    User = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    Gallery = models.ForeignKey(Gallery, on_delete=models.CASCADE)
    UploadDateTime = models.DateTimeField(default=None, null=True, editable=False)
    Comment = models.CharField(max_length=1024, blank=True, null=True)
    #NOTIFICATIONS NOT ADDED

    def __str__(self): return str(self.Gallery) + " - " + str(self.UploadDateTime)

class PhotoComment(models.Model):
    User = models.ForeignKey(User, on_delete=models.DO_NOTHING, default=1)
    Photo = models.ForeignKey(Photo, on_delete=models.CASCADE, default=1)
    UpdateDateTime = models.DateTimeField(auto_now_add=True, null=True, editable=False)
    Comment = models.CharField(max_length=1024, blank=True, null=True)

    # NOTIFICATIONS NOT ADDED
    def __str__(self): return str(self.Photo) + " - " + str(self.Comment)

class Follow(models.Model):
    FollowCond1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followed')
    FollowCond2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follower')

    # Cond2 can view Cond1
    # Follower can view followed
    # NOTIFICATIONS NOT ADDED
    # def __str__(self): return str(self.FollowCond2) + " can view content of " + str(self.FollowCond1)
    def __str__(self): return "FC1 =" + str(self.FollowCond1) + " FC2 = " + str(self.FollowCond2)

class Profile(models.Model):    # authorization demanded for sure
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    ProfilePhoto = models.ImageField(default='profile_pics/default.jpg',upload_to='profile_pics/',storage=ExternalStorage())
    RegisterDateTime = models.DateTimeField(auto_now_add=True, null=True, editable=False)
    BirthDate = models.DateField(null=True, blank=True, editable=True)
    Bio = models.CharField(default='', max_length=500, blank=True, null=True)
    FirstName = models.CharField(default='', max_length=20, blank=True, null=False)
    LastName = models.CharField(default='', max_length=30, blank=True, null=False)
    Sex = models.CharField(default=NOTANSWER, null=False, blank=False, max_length=2, choices=GENDER)

    def __str__(self): return str(self.user.username)   # this is what it is going to show

    # def save(self, *args, **kwargs):
    #     super(Profile, self).save(*args, **kwargs)
    #     pf = Image.open(self.ProfilePhoto.path)
    #
    #     if pf.height > 300 or pf.width > 300:   # overwriting existing images in specific size
    #         output_size = (300, 300)
    #         pf.thumbnail(output_size)
    #         pf.save(self.ProfilePhoto.path)