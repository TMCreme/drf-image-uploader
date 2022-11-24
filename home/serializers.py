from rest_framework import serializers
# from django.contrib.auth.models import User
# from django.contrib.auth.hashers import make_password

from .models import (
    UserImage, UserImageThumbnail
)


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


class UserImageCreateSerializer(serializers.ModelSerializer):
    # user = serializers.CharField(write_only=True)

    class Meta:
        model = UserImage
        fields = ["image", "name", "user"]


class DynamicFieldsModelSerializer(serializers.ModelSerializer):
    """
    A ModelSerializer that takes an additional `fields` argument that
    controls which fields should be displayed.
    """

    def __init__(self, *args, **kwargs):
        # Don't pass the 'fields' arg up to the superclass
        fields = kwargs.pop('fields', None)

        # Instantiate the superclass normally
        super().__init__(*args, **kwargs)

        if fields is not None:
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)


class UserImageThumbnailSerializer(DynamicFieldsModelSerializer, serializers.ModelSerializer):
    original_image_link = serializers.CharField(
        source='original_image.image', read_only=True
        )
    thumbnail_name = serializers.CharField(
        source='thumbnail.account_tier.name', read_only=True
    )

    class Meta:
        model = UserImageThumbnail
        fields = [
            'name', 'image',
            'date_created', 'user',
            'original_image_link',
            'thumbnail_name'
            ]



