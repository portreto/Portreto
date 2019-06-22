from rest_framework import serializers
from webmain.models import *

from rest_framework.exceptions import AuthenticationFailed, NotAcceptable

class GalleryReactionSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(validators=None)
    class Meta:
        model = GalleryReaction
        fields = '__all__'

    def create(self, validated_data = None):
        return GalleryReaction(**self.validated_data)

class PhotoReactionSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(validators=None)
    class Meta:
        model = PhotoReaction
        fields = '__all__'

    def create(self, validated_data = None):
        return PhotoReaction(**self.validated_data)

class GalleryCommentSerializer(serializers.ModelSerializer):
    # id = serializers.IntegerField(validators=None)
    class Meta:
        model = GalleryComment
        fields = '__all__'

    def create(self, validated_data = None):
        self.is_valid()
        comment = GalleryComment(**self.validated_data)
        comment.save()

        return comment

class PhotoCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhotoComment
        fields = '__all__'

    def create(self, validated_data = None):

        photo_comment = PhotoComment(**self.validated_data)
        photo_comment.save()

        return photo_comment

class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = '__all__'

    def create(self, validated_data = None):
        # self.validated_data.pop("id")
        follow = Follow(**self.validated_data)
        follow.save()

        return follow

class UserSerializer(serializers.ModelSerializer):

    # username = serializers.CharField(validators=None)
    # id = serializers.IntegerField(validators=None)

    class Meta:
        model = User
        fields = ['id','username']

    def create(self, validated_data = None):

        user = User(**self.validated_data)
        user.save()

        return user

class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(validators=None)
    # user = UserSerializer()
    # id = serializers.IntegerField(validators=None)
    class Meta:
        model = Profile
        fields = '__all__'

    def create(self, validated_data = None):

        prof = Profile(**self.validated_data)
        prof.save()

        return prof

    # def update(self, validated_data = None):
    #     print("\n\n UPDATING !!!!!!!!!!!! :  \n\n")

#Special Serializer for updating profile
class ProfileUpdateDeserializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        exclude = ('user',)

class GallerySerializer(serializers.ModelSerializer):
    GalleryOwner = UserSerializer(read_only=False)

    class Meta:
        model = Gallery
        fields = '__all__'
        # depth = 1

    def create(self, validated_data = None):
        gall = Gallery(**self.validated_data)
        #check for duplicates
        galleryName = gall.Name
        user_galleries = Gallery.objects.filter(GalleryOwner__username= gall.GalleryOwner, Name = galleryName)
        if len(user_galleries)>0:
            raise NotAcceptable
            return
        # Save Gallery
        gall.save()
        return gall

    def destroy(self):
        gall = Gallery(**self.validated_data)

        #get gallery
        gallery = Gallery.objects.get(GalleryOwner__username= gall.GalleryOwner, Name = gall.Name)
        gallery.delete()

        return gall

#Special Serializer for creating galleries
class GalleryDeserializer(serializers.ModelSerializer):
    class Meta:
        model = Gallery
        fields = '__all__'

    def create(self, validated_data = None):
        gall = Gallery(**self.validated_data)
        #check for duplicates
        galleryName = gall.Name
        user_galleries = Gallery.objects.filter(GalleryOwner__username= gall.GalleryOwner, Name = galleryName)
        if len(user_galleries)>0:
            raise NotAcceptable
            return
        gall.save()
        return gall


class PhotoSerializer(serializers.ModelSerializer):
    # id = serializers.IntegerField(validators=None)
    class Meta:
        model = Photo
        fields = '__all__'

    def create(self, validated_data = None):

        photo = Photo(**self.validated_data)
        photo.save()

        return photo