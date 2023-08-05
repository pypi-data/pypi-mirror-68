from import_export import resources

from . import models


class ItemSchemaResource(resources.ModelResource):
    class Meta:
        model = models.ItemSchema
        exclude = ('image',)


class BooleanFieldResource(resources.ModelResource):
    class Meta:
        model = models.BooleanField


class ChoicesFieldResource(resources.ModelResource):
    class Meta:
        model = models.ChoicesField
        exclude = ('default',)


class DateTimeFieldResource(resources.ModelResource):
    class Meta:
        model = models.DateTimeField


class FileFieldResource(resources.ModelResource):
    class Meta:
        model = models.FileField
        exclude = ('default',)


class ImagesFieldResource(resources.ModelResource):
    class Meta:
        model = models.ImagesField
        exclude = ('default',)


class ItemFieldResource(resources.ModelResource):
    class Meta:
        model = models.ItemField
        exclude = ('default',)


class NumberFieldResource(resources.ModelResource):
    class Meta:
        model = models.NumberField


class TextFieldResources(resources.ModelResource):
    class Meta:
        model = models.TextField


class CategoryResource(resources.ModelResource):
    class Meta:
        model = models.Category


class ChoiceResource(resources.ModelResource):
    class Meta:
        model = models.Choice

