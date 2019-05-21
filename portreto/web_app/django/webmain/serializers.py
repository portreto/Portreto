from rest_framework import serializers
from webmain.models import *

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
    id = serializers.IntegerField(validators=None)
    class Meta:
        model = GalleryComment
        fields = '__all__'

    def create(self, validated_data = None):
        return GalleryComment(**self.validated_data)

class PhotoCommentSerializer(serializers.ModelSerializer):

    id = serializers.IntegerField(validators=None)

    class Meta:
        model = PhotoComment
        fields = '__all__'

    def create(self, validated_data = None):
        return PhotoComment(**self.validated_data)

class FollowSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(validators=None)
    class Meta:
        model = Follow
        fields = '__all__'

    def create(self, validated_data = None):
        return Follow(**self.validated_data)

class UserSerializer(serializers.ModelSerializer):

    username = serializers.CharField(validators=None)
    id = serializers.IntegerField(validators=None)

    class Meta:
        model = User
        fields = ['id','username']

    def create(self, validated_data = None):
        return User(**self.validated_data)

class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    # user = UserSerializer()
    # id = serializers.IntegerField(validators=None)

    class Meta:
        model = Profile
        fields = '__all__'

    def create(self, validated_data = None):
        return Profile(**self.validated_data)

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
    # AlbumCover = serializers.CharField()
    # id = serializers.IntegerField()
    class Meta:
        model = Gallery
        fields = '__all__'

    def create(self, validated_data = None):
        return Gallery(**self.validated_data)

class GalleryDeserializer(serializers.ModelSerializer):
    AlbumCover = serializers.CharField()
    id = serializers.IntegerField()

    class Meta:
        model = Gallery
        fields = '__all__'

    def create(self, validated_data = None):
        return Gallery(**self.validated_data)

class PhotoSerializer(serializers.ModelSerializer):
    # id = serializers.IntegerField(validators=None)
    # Photo = serializers.CharField()
    class Meta:
        model = Photo
        fields = '__all__'

    def create(self, validated_data = None):
        return Photo(**self.validated_data)

class PhotoDeserializer(serializers.ModelSerializer):
    Photo = serializers.CharField()
    id = serializers.IntegerField(validators=None)
    # PhotoUrl = serializers.URLField(read_only=True,source='Photo.url')
    class Meta:
        model = Photo
        fields = '__all__'

    def create(self, validated_data = None):
        return Photo(**self.validated_data)
