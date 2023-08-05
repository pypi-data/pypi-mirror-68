from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from . import models
from .services import update_item, _field_params, ItemUpdater


@receiver(post_save, sender=models.Item)
def item_post_save(sender, instance: models.Item, **kwargs):
    update_item(instance)


def update_items(sender, instance, created=False, **kwargs):
    if instance is not None and created:
        schema = instance.item_schema
        item_updater = ItemUpdater(queryset=schema.items.all())
        item_updater.start()


for param in _field_params:
    post_save.connect(receiver=update_items, sender=param['field_model'])
    post_delete.connect(receiver=update_items, sender=param['field_model'])



