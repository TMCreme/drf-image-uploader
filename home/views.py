from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import UserImage, UserImageThumbnail
from .serializers import (
    UserImageSerializer,
    UserImageThumbnailSerializer,
    UserImageCreateSerializer
)
import os
from .utils import create_presigned_url


class UserImageThumbnailListView(generics.ListAPIView):
    # queryset = UserImageThumbnail.objects.filter(
    #     user=request.user
    # )
    serializer_class = UserImageThumbnailSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        image_obj = UserImageThumbnail.objects.filter(
                user=self.request.user
            )
        # if not self.request.user.account_tier.display_link_to_original_image:
        #     image_obj = image_obj.values(
        #         'name', 'image', 'date_created', 'user'
        #     )
        return image_obj

    def list(self, request):
        # Note the use of `get_queryset()` instead of `self.queryset`
        queryset = self.get_queryset()
        if not self.request.user.account_tier.display_link_to_original_image:
            serializer = UserImageThumbnailSerializer(
                queryset, fields=(
                    'name', 'image', 'date_created', 'user',
                    'thumbnail_name'),
                many=True
                )
        else:
            serializer = UserImageThumbnailSerializer(
                queryset,
                many=True
            )
        return Response(serializer.data)


class UserImageCreateView(generics.CreateAPIView):
    serializer_class = UserImageCreateSerializer
    permission_classes = [IsAuthenticated]

    # def post(self, request):
    #     request.data["user"] = request.user
    #     serializer = UserImageCreateSerializer(
    #         data=request.data
    #     )
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(
    #             {
    #                 "status": "success",
    #                 "message": "Image Uploaded Successfully",
    #                 "data": []
    #             },
    #             status.HTTP_200_OK
    #         )


class UserImageListView(generics.ListAPIView):
    serializer_class = UserImageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return UserImage.objects.filter(
            user=self.request.user
        )


class GenerateTempLink(APIView):
    permission_clsses = [IsAuthenticated]

    def post(self, request):
        image_obj = UserImage.objects.get(
                id=request.data["image_id"]
                ).image.file.name,
        # user = request.user
        original_image = image_obj[0]
        alive_duration = request.data["alive_duration"]
        presigned_url = create_presigned_url(
            original_image, alive_duration
        )
        return Response(
            {
                "status": "success",
                "message": "Link Generated Successfully",
                "data": presigned_url
            }
        )



# Create your views here.
