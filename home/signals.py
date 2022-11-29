from django.db.models.signals import post_save
from django.dispatch import receiver
from .tasks import create_thumbnail_task
from django.db import transaction
from django.core import serializers
from .models import UserImage


# The function receives a signal to create the thumbnails
# The function has been moved to Celery task
@receiver(post_save, sender=UserImage)
def create_thumbnail(sender, instance, **kwargs):
    print("Received the signal for thumbnail", instance.pk)
    # instance = serializers.serialize('json', [instance['pk'], ])
    create_thumbnail_task.delay(str(instance.pk))
    print("Signal sent to Celery Task for processing")


# post_save.connect(create_thumbnail, sender=UserImage)
