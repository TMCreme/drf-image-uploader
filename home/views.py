from django.shortcuts import render
from rest_framework import generics 
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import UserImage, UserImageThumbnail
from .serializers import (
    UserImageSerializer, UserImageThumbnailSerializer
)


class UserImageListView(generics.ListAPIView):
    # queryset = UserImageThumbnail.objects.filter(
    #     user=request.user
    # )
    serializer_class = UserImageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return UserImageThumbnail.objects.filter(
                user=self.request.user
            )

    def list(self, request):
        # Note the use of `get_queryset()` instead of `self.queryset`
        queryset = self.get_queryset()
        serializer = UserImageThumbnailSerializer(queryset, many=True)
        return Response(serializer.data)


class UserImageCreateView(generics.CreateAPIView):
    serializer_class = UserImageSerializer
    permission_classes = [IsAuthenticated]







# Create your views here.
