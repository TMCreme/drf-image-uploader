from rest_framework import serializers
# from django.contrib.auth.models import User
# from django.contrib.auth.hashers import make_password

from .models import UserImage, UserImageThumbnail


# class UserSerializer(serializers.HyperlinkedModelSerializer):

#     password = serializers.CharField(
#         write_only=True,
#         required=True,
#         help_text='Leave empty if no change needed',
#         style={'input_type': 'password', 'placeholder': 'Password'}
#     )

#     class Meta:
#         model = User
#         fields = ('username', 'password')

#     def create(self, validated_data):
#         validated_data['password'] = make_password(
#             validated_data.get('password')
#             )
#         return super(UserSerializer, self).create(validated_data)


class UserImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserImage
        fields = "__all__"


class UserImageThumbnailSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserImageThumbnail
        fields = "__all__"
