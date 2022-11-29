from django.core.files import File
from django.core import serializers
import celery
from celery import shared_task
from celery.utils.log import get_task_logger
from datetime import datetime
from pathlib import Path
from io import BytesIO
import os
from PIL import Image
import json

from .models import (
    ImageThumbnail, UserImageThumbnail,
    UserImage
)

logger = get_task_logger(__name__)


@shared_task
def create_thumbnail_task(instance):
    logger.debug("Received the call from the signal")
    logger.debug(instance)
    # instance = serializers.deserialize('json', instance)
    # logger.debug(instance)
    instance = UserImage.objects.get(id=int(instance))
    account_tier = instance.user.account_tier
    new_image = Image.open(instance.image)
    height_list = ImageThumbnail.objects.filter(
        account_tier=account_tier
        ).values('id', 'height')
    logger.debug("Starting the creation of thumbnails")
    print("Starting the creation of thumbnails")
    for item in height_list:
        image_name = "{}/{}_{}_{}_{}_{}".format(
            "media",
            instance.user.username,
            instance.user.account_tier.name,
            instance.name, item['height'],
            datetime.now().strftime("%Y%m%d"))
        new_size = new_image.size
        new_image.thumbnail(
                (new_size[0], int(item['height'])))
        img_name_split = Path(instance.image.file.name).name.split(".")
        buffer = BytesIO()
        new_image.save(buffer, format=img_name_split[-1])
        file_object = File(buffer)
        new_image.save(
                image_name + "."+ img_name_split[-1],
                file_object
            ),
        print("Image thumbnail creation done")
        userthumbnail = UserImageThumbnail.objects.create(
            name=image_name[6:] + "." + img_name_split[-1],
            thumbnail=ImageThumbnail.objects.get(id=item['id']),
            user=instance.user,
            original_image = instance
        )
        userthumbnail.image = image_name + "." + img_name_split[-1]
        userthumbnail.save()
        os.remove(image_name + "." + img_name_split[-1])
        print("Remove temp file from OS")
    return {"status": True}
