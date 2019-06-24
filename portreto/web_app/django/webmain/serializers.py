from rest_framework import serializers
from webmain.models import *
from django.conf.global_settings import MEDIA_URL

class UserSerializer(serializers.ModelSerializer):

    username = serializers.CharField(validators=None)
    id = serializers.IntegerField(validators=None)

    class Meta:
        model = User
        fields = ['id','username','email']

    def create(self, validated_data = None):
        return User(**self.validated_data)

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

class GalleryCommentDeserializer(serializers.ModelSerializer):
    id = serializers.IntegerField(validators=None)
    User = UserSerializer(validators=None)

    class Meta:
        model = GalleryComment
        fields = '__all__'

    def create(self, validated_data = None):
        self.is_valid()

        user_dt = self.validated_data.pop("User")
        user_serializer = UserSerializer(data=user_dt)
        user_serializer.is_valid()

        user = user_serializer.create()
        return GalleryComment(User = user, **self.validated_data)

class GalleryCommentSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(validators=None)
    User = serializers.CharField()

    class Meta:
        model = GalleryComment
        fields = '__all__'

class PhotoCommentDeserializer(serializers.ModelSerializer):
    id = serializers.IntegerField(validators=None)
    User = UserSerializer()

    class Meta:
        model = PhotoComment
        fields = '__all__'

    def create(self, validated_data = None):
        self.is_valid()

        user_dt = self.validated_data.pop("User")
        user_serializer = UserSerializer(data=user_dt)
        user_serializer.is_valid()

        user = user_serializer.create()


        return PhotoComment(User = user, **self.validated_data)

class PhotoCommentSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(validators=None)
    User = serializers.CharField()

    class Meta:
        model = PhotoComment
        fields = '__all__'

class FollowSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(validators=None)

    class Meta:
        model = Follow
        fields = '__all__'

    def create(self, validated_data = None):
        self.validate(self)
        return Follow(**self.validated_data)

class ProfileSerializer(serializers.ModelSerializer):
    user = serializers.CharField(allow_null=False)

    # user = UserSerializer()
    # id = serializers.IntegerField(validators=None)

    class Meta:
        model = Profile
        fields = '__all__'

    # def create(self, validated_data = None):
    #     self.is_valid()
    #
    #     image = self.validated_data.pop("ProfilePhoto")
    #     # TODO Default image
    #     if image == None:
    #         image = '/media/profile_pics/default.jpg'
    #
    #
    #     return Profile(ProfilePhoto = image,**self.validated_data)

class ProfileDeserializer(serializers.ModelSerializer):
    ProfilePhoto = serializers.CharField(allow_null=True)
    user = UserSerializer()
    id = serializers.IntegerField(validators=None)

    class Meta:
        model = Profile
        fields = '__all__'

    def create(self, validated_data = None):

        self.is_valid()

        user_dt = self.validated_data.pop("user")
        user_serializer = UserSerializer(data=user_dt)
        user_serializer.is_valid()

        user = user_serializer.create()

        image = self.validated_data.pop("ProfilePhoto")

        if image == None:
            image = '/media/profile_pics/default.jpg'


        return Profile(ProfilePhoto = image, user = user, **self.validated_data)

class GallerySerializer(serializers.ModelSerializer):
    # AlbumCover = serializers.CharField()
    # id = serializers.IntegerField()

    GalleryOwner = UserSerializer()

    class Meta:
        model = Gallery
        fields = '__all__'

    def create(self, validated_data = None):
        return Gallery(**self.validated_data)

class GalleryDeserializer(serializers.ModelSerializer):
    AlbumCover = serializers.CharField()
    id = serializers.IntegerField()
    GalleryOwner = UserSerializer()

    class Meta:
        model = Gallery
        fields = '__all__'

    def create(self, validated_data = None):
        self.is_valid()
        user_dt = self.validated_data.pop("GalleryOwner")
        user_serializer = UserSerializer(data=user_dt)
        user_serializer.is_valid()
        GalleryOwner = user_serializer.create()
        return Gallery(GalleryOwner = GalleryOwner, **self.validated_data)

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
    id = serializers.IntegerField(validators=None,)
    # PhotoUrl = serializers.URLField(read_only=True,source='Photo.url')
    class Meta:
        model = Photo
        fields = '__all__'

    def create(self, validated_data = None):
        return Photo(**self.validated_data)
