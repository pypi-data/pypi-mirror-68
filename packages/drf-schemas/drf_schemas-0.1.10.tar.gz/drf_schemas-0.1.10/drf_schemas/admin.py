from django.contrib import admin

from . import models


@admin.register(models.DateTimeField)
class DateTimeFieldAdmin(admin.ModelAdmin):
    pass


@admin.register(models.DateTimeValue)
class DateTimeValueAdmin(admin.ModelAdmin):
    pass


@admin.register(models.NumberField)
class NumberFieldAdmin(admin.ModelAdmin):
    pass


@admin.register(models.NumberValue)
class NumberValueAdmin(admin.ModelAdmin):
    pass


@admin.register(models.TextField)
class TextFieldAdmin(admin.ModelAdmin):
    pass


@admin.register(models.TextValue)
class TextValueAdmin(admin.ModelAdmin):
    pass


@admin.register(models.BooleanField)
class BoolFieldAdmin(admin.ModelAdmin):
    pass


@admin.register(models.BooleanValue)
class BooleanValueAdmin(admin.ModelAdmin):
    pass


@admin.register(models.ChoicesField)
class ChoicesFieldAdmin(admin.ModelAdmin):
    pass


@admin.register(models.ChoicesValue)
class ChoicesValueAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Choice)
class ChoiceAdmin(admin.ModelAdmin):
    pass


@admin.register(models.ImagesField)
class ImagesFieldAdmin(admin.ModelAdmin):
    pass


@admin.register(models.ImagesValue)
class ImagesValueFieldAdmin(admin.ModelAdmin):
    pass


@admin.register(models.FileField)
class FileFieldAdmin(admin.ModelAdmin):
    pass


@admin.register(models.FileValue)
class FileValueAdmin(admin.ModelAdmin):
    pass


@admin.register(models.ItemField)
class ItemFieldAdmin(admin.ModelAdmin):
    pass


@admin.register(models.ItemValue)
class ItemValueFieldAdmin(admin.ModelAdmin):
    pass


@admin.register(models.ItemSchema)
class ItemSchemaAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Item)
class ItemAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Image)
class ImageAdmin(admin.ModelAdmin):
    pass


@admin.register(models.File)
class FileAdmin(admin.ModelAdmin):
    pass

