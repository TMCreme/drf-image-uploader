from time import time
from django.db import models
from django.contrib.auth.models import (
    AbstractUser, AbstractBaseUser
)
from django.urls import reverse
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.core.files import File
from pathlib import Path
import uuid
from PIL import Image
from io import BytesIO
from django.utils import timezone
from datetime import datetime, timedelta
import os
import shutil


# The account tiers or plans to be given to users.
class AccountTier(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=100, unique=True, db_index=True)
    display_link_to_original_image = models.BooleanField(default=False)
    generate_expiring_links = models.BooleanField(default=False)

    def __str__(self):
        return self.name


# The thumbnails under a particular account tier.
class ImageThumbnail(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    account_tier = models.ForeignKey(AccountTier, on_delete=models.CASCADE)
    height = models.CharField(
        max_length=5,
        help_text="Enter height of image thumbnail"
        )


# An extension of the Django abstract user
class User(AbstractUser):
    account_tier = models.ForeignKey(
        AccountTier, on_delete=models.PROTECT, null=True
        )

    # This function is to hash password
    def save(self, *args, **kwargs):
        create = True if self.id is None else False

        if create:
            self.set_password(self.password)
        super(User, self).save(*args, **kwargs)


# Creating custom upload paths for user and it's account tier
def get_upload_path(instance, filename):
    return "useruploads/{0}/{1}/{2}".format(
        instance.user.account_tier,
        instance.user.username, filename)


class UserImage(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    image_uuid = models.UUIDField(
        unique=True, db_index=True, default=uuid.uuid4, editable=False
        )
    name = models.CharField(max_length=250, db_index=True)
    # slug = models.SlugField()
    image = models.ImageField(upload_to=get_upload_path)

    def get_absolute_url(self):
        return reverse("user_image", kwargs={"pk": self.pk})

    def __str__(self) -> str:
        return self.name


# This model creates individual records for each
# thumbnail under the account tier
class UserImageThumbnail(models.Model):
    date_created = models.DateTimeField(auto_now_add=True, db_index=True)
    date_modified = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to=get_upload_path)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    thumbnail = models.ForeignKey(ImageThumbnail, on_delete=models.CASCADE)
    name = models.CharField(max_length=500)
    original_image = models.ForeignKey(
        UserImage, on_delete=models.CASCADE
        )

    def __str__(self) -> str:
        return self.name


# The function receives a signal to create the thumbnails
# A more scalable approach will be to use django-celery
@receiver(post_save, sender=UserImage)
def create_thumbnail(sender, instance, **kwargs):
    account_tier = instance.user.account_tier
    new_image = Image.open(instance.image)
    height_list = ImageThumbnail.objects.filter(
        account_tier=account_tier
        ).values('id', 'height')
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
        userthumbnail = UserImageThumbnail.objects.create(
            name=image_name[6:] + "." + img_name_split[-1],
            thumbnail=ImageThumbnail.objects.get(id=item['id']),
            user=instance.user,
            original_image = instance
        )
        userthumbnail.image = image_name + "." + img_name_split[-1]
        userthumbnail.save()
        os.remove(image_name + "." + img_name_split[-1])
























# Create your models here.
