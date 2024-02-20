from .models import Category
from django.db.models.signals import pre_delete
from django.dispatch import receiver


@receiver(pre_delete, sender=Category)
def delete_model_images(sender, instance, **kwargs):
    if instance.category_img:
        instance.category_img.delete(save=False)