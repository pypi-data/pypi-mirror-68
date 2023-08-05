from django.db import models
from django.conf import settings
from django.utils.functional import cached_property


class TrackTimeModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Field(TrackTimeModel):
    name = models.CharField(max_length=255)
    required = models.BooleanField(blank=True, default=True)
    order = models.IntegerField(blank=True, default=0)
    help = models.TextField(blank=True, default='')
    config = models.TextField(blank=True, default='{}')

    def __str__(self):
        return f'{self.name} [{self.pk}]'

    class Meta:
        abstract = True


class Value(TrackTimeModel):

    def __str__(self):
        # noinspection PyUnresolvedReferences
        return f'{self.__class__} [{self.pk}]'

    @cached_property
    def order(self):
        # noinspection PyUnresolvedReferences
        return self.field.order

    class Meta:
        abstract = True


class TextField(Field):

    default = models.TextField(blank=True, default='')

    item_schema = models.ForeignKey(
        'ItemSchema',
        on_delete=models.CASCADE,
        related_name='text_fields'
    )


class TextValue(Value):

    value = models.TextField(blank=True, default='')

    field = models.ForeignKey(
        'TextField',
        on_delete=models.CASCADE,
        related_name='text_values'
    )

    item = models.ForeignKey(
        'Item',
        on_delete=models.CASCADE,
        related_name='text_values'
    )


class DateTimeField(Field):

    default = models.DateTimeField(blank=True, null=True)
    min_value = models.DateTimeField(blank=True, null=True)
    max_value = models.DateTimeField(blank=True, null=True)

    item_schema = models.ForeignKey(
        'ItemSchema',
        on_delete=models.CASCADE,
        related_name='datetime_fields'
    )


class DateTimeValue(Value):
    value = models.DateTimeField(blank=True, null=True)
    field = models.ForeignKey(
        'DateTimeField',
        on_delete=models.CASCADE,
        related_name='datetime_values'
    )
    item = models.ForeignKey(
        'Item',
        on_delete=models.CASCADE,
        related_name='datetime_values'
    )


class NumberField(Field):

    default = models.FloatField(blank=True, null=True)
    min_value = models.FloatField(blank=True, null=True)
    max_value = models.FloatField(blank=True, null=True)

    item_schema = models.ForeignKey(
        'ItemSchema',
        on_delete=models.CASCADE,
        related_name='number_fields'
    )


class NumberValue(Value):
    value = models.FloatField(blank=True, null=True)
    field = models.ForeignKey(
        'NumberField',
        on_delete=models.CASCADE,
        related_name='number_values'
    )
    item = models.ForeignKey(
        'Item',
        on_delete=models.CASCADE,
        related_name='number_values'
    )


class BooleanField(Field):

    default = models.BooleanField(blank=True, null=True)

    item_schema = models.ForeignKey(
        'ItemSchema',
        on_delete=models.CASCADE,
        related_name='boolean_fields'
    )


class BooleanValue(Value):
    value = models.BooleanField(blank=True, null=True)
    field = models.ForeignKey(
        'BooleanField',
        on_delete=models.CASCADE,
        related_name='boolean_values'
    )
    item = models.ForeignKey(
        'Item',
        on_delete=models.CASCADE,
        related_name='boolean_values'
    )


class Choice(models.Model):
    name = models.CharField(max_length=255)
    field = models.ForeignKey(
        'ChoicesField',
        on_delete=models.CASCADE,
        related_name='choices'
    )


class ChoicesField(Field):

    multi = models.BooleanField(blank=True, default=False)

    default = models.ManyToManyField(
        'Choice',
        related_name='field_default'
    )

    item_schema = models.ForeignKey(
        'ItemSchema',
        on_delete=models.CASCADE,
        related_name='choices_fields'
    )


class ChoicesValue(Value):
    value = models.ManyToManyField(
        'Choice',
        related_name='field_values'
    )
    field = models.ForeignKey(
        'ChoicesField',
        on_delete=models.CASCADE,
        related_name='choices_values'
    )
    item = models.ForeignKey(
        'Item',
        on_delete=models.CASCADE,
        related_name='choices_values'
    )


class Image(TrackTimeModel):
    image = models.ImageField()
    size_bytes = models.IntegerField(blank=True, default=0)
    height = models.IntegerField(blank=True, default=0)
    width = models.IntegerField(blank=True, default=0)


class ImagesField(Field):

    multi = models.BooleanField(blank=True, default=False)

    default = models.ManyToManyField(
        'Image',
        related_name='defaults'
    )

    item_schema = models.ForeignKey(
        'ItemSchema',
        on_delete=models.CASCADE,
        related_name='images_fields'
    )


class ImagesValue(Value):
    value = models.ManyToManyField(
        'Image',
        related_name='images_values'
    )
    field = models.ForeignKey(
        'ImagesField',
        on_delete=models.CASCADE,
        related_name='images_values'
    )
    item = models.ForeignKey(
        'Item',
        on_delete=models.CASCADE,
        related_name='images_values'
    )


class File(TrackTimeModel):
    file = models.FileField()
    size_bytes = models.IntegerField(blank=True, default=0)


class FileField(Field):

    multi = models.BooleanField(blank=True, default=False)

    default = models.ManyToManyField(
        'File',
        related_name='defaults'
    )

    item_schema = models.ForeignKey(
        'ItemSchema',
        on_delete=models.CASCADE,
        related_name='file_fields'
    )


class FileValue(Value):
    value = models.ManyToManyField(
        'File',
        related_name='file_values'
    )
    field = models.ForeignKey(
        'FileField',
        on_delete=models.CASCADE,
        related_name='file_values'
    )
    item = models.ForeignKey(
        'Item',
        on_delete=models.CASCADE,
        related_name='file_values'
    )


class ItemField(Field):

    multi = models.BooleanField(blank=True, default=False)

    default = models.ManyToManyField(
        'Item',
        related_name='field_default'
    )

    target_schema = models.ForeignKey(
        'ItemSchema',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='target_fields'
    )

    item_schema = models.ForeignKey(
        'ItemSchema',
        on_delete=models.CASCADE,
        related_name='item_fields'
    )


class ItemValue(Value):

    value = models.ManyToManyField(
        'Item',
        related_name='target_values'
    )
    field = models.ForeignKey(
        'ItemField',
        on_delete=models.CASCADE,
        related_name='values'
    )
    item = models.ForeignKey(
        'Item',
        on_delete=models.CASCADE,
        related_name='item_values'
    )


class Category(TrackTimeModel):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, default='')
    parent = models.ForeignKey(
        'Category',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='children'
    )


class ItemSchema(TrackTimeModel):

    name = models.CharField(max_length=255)
    category = models.ForeignKey(
        'Category',
        on_delete=models.SET_NULL,
        null=True,
        related_name='schemas'
    )
    image = models.ForeignKey(
        'Image',
        on_delete=models.SET_NULL,
        null=True,
        related_name='schema_images'
    )
    config = models.TextField(blank=True, default='{}')

    def __str__(self):
        return f'[{self.pk}] {self.name}'

    @cached_property
    def items_count(self):
        return self.items.all().count()


class Item(TrackTimeModel):

    schema = models.ForeignKey(
        'ItemSchema',
        on_delete=models.CASCADE,
        related_name='items'
    )

    def __str__(self):
        return f'[{self.pk}] Item'
