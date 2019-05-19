from rest_framework import serializers
from webmain.models import *

class GallerySerializer(serializers.ModelSerializer):

    # AlbumCover = serializers.ImageField(use_url=True, allow_empty_file=True)
    def validate_albumcover(self, value):
        print("========================================VALIDATING==========================================")
        return value

    class Meta:
        model = Gallery
        fields = '__all__'

class GalleryReactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = GalleryReaction
        fields = '__all__'

    def create(self):
        return GalleryReaction(**self.validated_data)

class PhotoSerializer(serializers.ModelSerializer):

    # PhotoUrl = serializers.URLField(read_only=True,source='Photo.url')
    class Meta:
        model = Photo
        fields = '__all__'

    def create(self):
        return Photo(**self.validated_data)

class PhotoReactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhotoReaction
        fields = '__all__'

    def create(self):
        return PhotoReaction(**self.validated_data)

class GalleryCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = GalleryComment
        fields = '__all__'

    def create(self):
        return GalleryComment(**self.validated_data)

class PhotoCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhotoComment
        fields = '__all__'

    def create(self):
        return PhotoComment(**self.validated_data)

class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = '__all__'

    def create(self):
        return Follow(**self.validated_data)

class UserSerializer(serializers.ModelSerializer):

    username = serializers.CharField(validators=None)
    id = serializers.IntegerField(validators=None)

    class Meta:
        model = User
        fields = ['id','username']

    def create(self):
        return User(**self.validated_data)


class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    # user = UserSerializer()

    class Meta:
        model = Profile
        fields = '__all__'

    def create(self):
        return Profile(**self.validated_data)

class ProfileDeserializer(serializers.ModelSerializer):
    ProfilePhoto = serializers.CharField()
    user = UserSerializer()

    class Meta:
        model = Profile
        fields = '__all__'

    def create(self):
        # print ("VALIDATED_DATA"+"="*40+"\n"+str(self.validated_data))
        user_data = self.validated_data.pop('user')
        user = User(**user_data)
        return Profile(user = user, **self.validated_data)