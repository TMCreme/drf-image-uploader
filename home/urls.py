from django.urls import path, re_path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path(
        "api-list-images/",
        views.UserImageListView.as_view(),
        name="api-list-images"),
    path(
        "api-upload-image/",
        views.UserImageCreateView.as_view(),
        name="api-upload-image"
    ),
    path(
        "api-list-image-thumbnail/",
        views.UserImageThumbnailListView.as_view(),
        name="api-list-image-thumbnail"
    ),
    path(
        "api-generate-temp-link/",
        views.GenerateTempLink.as_view(),
        name="api-generate-temp-link"
    )
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
