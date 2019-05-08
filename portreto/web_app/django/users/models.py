"""
    SK Edit
"""

from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Galleries(models.Model):
    #THIS DOESNOT WORK QUITE RIGHT
    # PRIVACY = (
    #     ("pv", "private"),
    #     ("pu", "public"),
    # )
    GalleryOwner = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    Name = models.CharField(max_length=75)
    Description = models.CharField(default='', null=True, blank=True, max_length=1024)
    Visibility = models.CharField(default='pu', null=True, blank=True, max_length=2)
    UploadDateTime = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self): return str(self.Name) + " - " + str(self.GalleryOwner)


# class Photo(models.Model):
#     Gallery = models.ForeignKey(Gallery, on_delete=models.CASCADE, default=1, null=True, blank=True)
#     UploadDateTime = models.DateTimeField(auto_now_add=True, null=True)
#     UUID = models.CharField(max_length=1024)
#     Location = models.CharField(default='', blank=True, null=True, max_length=100)
#     Description = models.CharField(default='', blank=True, null=True, max_length=1024)
#
#     def __str__(self): return str(self.Gallery) + " - " + self.UUID
#
#
#
#
# class Profile(models.Model):
#     User = models.OneToOneField(User, on_delete=models.CASCADE)
#     AuthService = models.CharField(max_length=100, blank=True, default='')
#     AuthServiceUserId = models.PositiveIntegerField(blank=True, default=1)
#     ProfilePhoto = models.ForeignKey(Photo, on_delete=models.SET_DEFAULT, default=None, null=True, blank=True)\
#
#     @property
#     def FullName(self): return self.User.first_name + ' ' + self.User.last_name
#
#     def __str__(self): return self.FullName
#
#
# class Friendship(models.Model):
#     User = models.ForeignKey('auth.User', default=1, on_delete=models.CASCADE, related_name='User')
#     Friend = models.ForeignKey('auth.User', default=1, on_delete=models.CASCADE, related_name='Friend')
#
#     def __str__(self): return str(self.User) + " -> " + str(self.Friend)
#
#
# class GalleryComment(models.Model):
#     User = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
#     Gallery = models.ForeignKey(Gallery, on_delete=models.CASCADE, default=1)
#     UploadDateTime = models.DateTimeField(default=None, null=True)
#     Text = models.CharField(max_length=1024)
#
#     def __str__(self): return str(self.Gallery) + " - " + str(self.UploadDateTime)
#
#
# class PhotoComment(models.Model):
#     User = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
#     Photo = models.ForeignKey(Photo, on_delete=models.CASCADE, default=1)
#     UploadDateTime = models.DateTimeField(auto_now_add=True, null=True)
#     Text = models.CharField(max_length=1024)
#
#     def __str__(self): return str(self.Photo) + " - " + str(self.UploadDateTime)
#
#
# class Like(models.Model):
#     User = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
#     Photo = models.ForeignKey(Photo, on_delete=models.CASCADE, default=1)
#
#     def __str__(self): return str(User) + " - " + str(Photo)