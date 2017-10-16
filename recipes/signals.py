from .models import Recipe
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver


@receiver(post_save, sender=Recipe)
def index_post(sender, instance, **kwargs):
    instance.indexing()


@receiver(pre_delete, sender=Recipe)
def delete_post(sender, instance, **kwargs):
    instance.es_delete()
