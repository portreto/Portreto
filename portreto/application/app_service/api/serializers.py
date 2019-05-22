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
    user = UserSerializer()
    # user = UserSerializer()
    # id = serializers.IntegerField(validators=None)

    class Meta:
        model = Profile
        fields = '__all__'

    def create(self, validated_data = None):

        prof = Profile(**self.validated_data)
        prof.save()

        return prof

class ProfileDeserializer(serializers.ModelSerializer):
    ProfilePhoto = serializers.CharField()
    user = UserSerializer()
    id = serializers.IntegerField(validators=None)

    class Meta:
        model = Profile
        fields = '__all__'

    def create(self, validated_data = None):
        # print ("VALIDATED_DATA"+"="*40+"\n"+str(self.validated_data))
        user_data = self.validated_data.pop('user')
        user = User(**user_data)
        return Profile(user = user, **self.validated_data)

class GallerySerializer(serializers.ModelSerializer):
    GalleryOwner = UserSerializer(read_only=False)

    class Meta:
        model = Gallery
        fields = '__all__'

    def create(self, validated_data = None):
        gall = Gallery(**self.validated_data)

        #check for duplicates

        galleryName = gall.Name
        print("\n\n\n\nGALLERY NAME" + "*" * 80 + str(galleryName) + "\n\n\n\n")

        user_galleries = Gallery.objects.filter(GalleryOwner__username= gall.GalleryOwner, Name = galleryName)

        print("\n\n\n\nUSER GALLERIES" + "*" * 80 + str(user_galleries) + "\n\n\n\n")

        if len(user_galleries)>0:
            raise NotAcceptable
            return

        gall.save()
        return gall

    def destroy(self):
        gall = Gallery(**self.validated_data)

        #check for duplicates

        galleryName = gall.Name

        user_galleries = Gallery.objects.filter(GalleryOwner__username= gall.GalleryOwner, Name = galleryName)


        if len(user_galleries)>0:
            raise NotAcceptable
            return

        gall.save()

        return gall

class GallerySerializerNoFk(serializers.ModelSerializer):
    class Meta:
        model = Gallery
        fields = '__all__'

    def create(self, validated_data = None):
        gall = Gallery(**self.validated_data)
        #check for duplicates
        galleryName = gall.Name
        print("\n\n\n\nGALLERY NAME" + "*" * 80 + str(galleryName) + "\n\n\n\n")
        user_galleries = Gallery.objects.filter(GalleryOwner__username= gall.GalleryOwner, Name = galleryName)
        print("\n\n\n\nUSER GALLERIES" + "*" * 80 + str(user_galleries) + "\n\n\n\n")
        if len(user_galleries)>0:
            raise NotAcceptable
            return
        gall.save()
        return gall

    def destroy(self):
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

class PhotoDeserializer(serializers.ModelSerializer):
    Photo = serializers.CharField()

    class Meta:
        model = Photo
        fields = '__all__'

    def create(self, validated_data = None):
        return Photo(**self.validated_data)
