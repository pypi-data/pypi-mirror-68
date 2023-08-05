import json

from rest_framework import serializers
from . import models


class MaskFieldSerializer(serializers.ModelSerializer):

    def __init__(self, *args, **kwargs):
        # Don't pass the 'fields' arg up to the superclass
        fields = kwargs.pop('fields', None)

        # Instantiate the superclass normally
        super(MaskFieldSerializer, self).__init__(*args, **kwargs)

        if fields is not None:
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)


class JSONField(serializers.Field):
    default_error_messages = {
        'invalid': 'Value must be valid JSON.'
    }

    def to_internal_value(self, data):
        try:
            data = json.dumps(data)
        except (TypeError, ValueError):
            self.fail('invalid')
        return data

    def to_representation(self, value):
        try:
            value = json.loads(value)
        except (TypeError, ValueError):
            self.fail('invalid')
        return value


class TrackTimeSerializer:
    created_at = serializers.DateTimeField(
        read_only=True,
        help_text='Date and time when instance was created'
    )
    updated_at = serializers.DateTimeField(
        read_only=True,
        help_text='Date and time when instance was updated'
    )

    class Meta:
        fields = (
            'created_at',
            'updated_at'
        )


class FieldSerializer(MaskFieldSerializer, TrackTimeSerializer):

    # Required
    name = serializers.CharField(
        required=True,
        help_text='Field name'
    )
    item_schema = serializers.PrimaryKeyRelatedField(
        queryset=models.ItemSchema.objects.all(),
        help_text='Schema ID this field belongs to'
    )

    # Optional
    required = serializers.BooleanField(
        required=False,
        default=True,
        help_text='Whether filling this field is mandatory on item creation'
    )
    order = serializers.IntegerField(
        required=False,
        default=0,
        help_text='Display priority of this field'
    )
    help = serializers.CharField(
        required=False,
        allow_blank=True,
        help_text='Help text of this field to show to the user'
    )
    config = JSONField(required=False)

    class Meta:
        fields = TrackTimeSerializer.Meta.fields + (
            'name',
            'required',
            'order',
            'help',
            'item_schema',
            'config',
        )


class ValueSerializer(MaskFieldSerializer, TrackTimeSerializer):

    item = serializers.PrimaryKeyRelatedField(
        queryset=models.Item.objects.all(),
        help_text='Item ID this value belongs to'
    )

    order = serializers.IntegerField(
        read_only=True,
        help_text='Display priority of this value'
    )

    class Meta:
        fields = TrackTimeSerializer.Meta.fields + ('item', 'order')


class DateTimeFieldSerializer(FieldSerializer):

    default = serializers.DateTimeField(
        required=False,
        allow_null=True,
        help_text='Field default value'
    )
    min_value = serializers.DateTimeField(
        required=False,
        allow_null=True,
        help_text='Field minimum value'
    )
    max_value = serializers.DateTimeField(
        required=False,
        allow_null=True,
        help_text='Field maximum value'
    )

    class Meta:
        model = models.DateTimeField
        fields = FieldSerializer.Meta.fields + (
            'id',
            'default',
            'min_value',
            'max_value'
        )


class DateTimeValueSerializer(ValueSerializer):

    value = serializers.DateTimeField(
        required=False,
        allow_null=True,
        help_text='Field value'
    )
    field = serializers.PrimaryKeyRelatedField(
        queryset=models.DateTimeField.objects.all(),
        help_text='Field ID this value belongs to'
    )

    class Meta:
        model = models.DateTimeValue
        fields = ValueSerializer.Meta.fields + (
            'id',
            'value',
            'field'
        )


class NumberFieldSerializer(FieldSerializer):

    default = serializers.FloatField(
        required=False,
        allow_null=True,
        help_text='Field default value'
    )
    min_value = serializers.FloatField(
        required=False,
        allow_null=True,
        help_text='Field minimum value'
    )
    max_value = serializers.FloatField(
        required=False,
        allow_null=True,
        help_text='Field maximum value'
    )

    class Meta:
        model = models.NumberField
        fields = FieldSerializer.Meta.fields + (
            'id',
            'default',
            'min_value',
            'max_value'
        )


class NumberValueSerializer(ValueSerializer):

    value = serializers.FloatField(
        required=False,
        allow_null=True,
        help_text='Field value'
    )
    field = serializers.PrimaryKeyRelatedField(
        queryset=models.NumberField.objects.all(),
        help_text='Field ID this value belongs to'
    )

    class Meta:
        model = models.NumberValue
        fields = ValueSerializer.Meta.fields + (
            'id',
            'value',
            'field'
        )


class TextFieldSerializer(FieldSerializer):

    default = serializers.CharField(
        required=False,
        allow_blank=True,
        help_text='Field default value'
    )

    class Meta:
        model = models.TextField
        fields = FieldSerializer.Meta.fields + (
            'id',
            'default'
        )


class TextValueSerializer(ValueSerializer):

    value = serializers.CharField(
        required=False,
        allow_blank=True,
        help_text='Field value',
        trim_whitespace=False
    )

    field = serializers.PrimaryKeyRelatedField(
        queryset=models.TextField.objects.all(),
        help_text='Field ID this value belongs to'
    )

    class Meta:
        model = models.TextValue
        fields = ValueSerializer.Meta.fields + (
            'id',
            'value',
            'field'
        )


class BooleanFieldSerializer(FieldSerializer):

    default = serializers.BooleanField(
        required=False,
        allow_null=True,
        help_text='Field default value'
    )

    class Meta:
        model = models.BooleanField
        fields = FieldSerializer.Meta.fields + (
            'id',
            'default'
        )


class BooleanValueSerializer(ValueSerializer):

    value = serializers.BooleanField(
        required=False,
        allow_null=True,
        help_text='Field value'
    )
    field = serializers.PrimaryKeyRelatedField(
        queryset=models.BooleanField.objects.all(),
        help_text='Field ID this value belongs to'
    )

    class Meta:
        model = models.BooleanValue
        fields = ValueSerializer.Meta.fields + (
            'id',
            'value',
            'field'
        )


class ChoiceSerializer(MaskFieldSerializer):

    name = serializers.CharField(
        help_text='Choice label'
    )
    field = serializers.PrimaryKeyRelatedField(
        queryset=models.ChoicesField.objects.all(),
        help_text='Field ID this choice belongs to'
    )

    class Meta:
        model = models.Choice
        fields = (
            'id',
            'name',
            'field'
        )


class ChoicesFieldSerializer(FieldSerializer):

    default = serializers.PrimaryKeyRelatedField(
        queryset=models.Choice.objects.all(),
        many=True,
        required=False,
        help_text='Default choices IDs'
    )
    choices = serializers.PrimaryKeyRelatedField(
        queryset=models.Choice.objects.all(),
        many=True,
        required=False,
        help_text='Allowed choices IDs'
    )
    multi = serializers.BooleanField(
        required=False,
        help_text='Whether to allow multi choice selection or not'
    )

    class Meta:
        model = models.ChoicesField
        fields = FieldSerializer.Meta.fields + (
            'id',
            'default',
            'choices',
            'multi'
        )


class ChoicesValueSerializer(ValueSerializer):

    value = serializers.PrimaryKeyRelatedField(
        queryset=models.Choice.objects.all(),
        many=True,
        required=False,
        help_text='Selected choices IDs'
    )
    field = serializers.PrimaryKeyRelatedField(
        queryset=models.ChoicesField.objects.all(),
        help_text='Field ID this value belongs to'
    )

    class Meta:
        model = models.BooleanValue
        fields = ValueSerializer.Meta.fields + (
            'id',
            'value',
            'field'
        )


class ImageSerializer(serializers.ModelSerializer):

    size_bytes = serializers.IntegerField(
        read_only=True,
        help_text='Image size in bytes'
    )
    height = serializers.IntegerField(
        read_only=True,
        help_text='Image height in pixels'
    )
    width = serializers.IntegerField(
        read_only=True,
        help_text='Image width in pixels'
    )

    class Meta:
        model = models.Image
        fields = (
            'id',
            'image',
            'size_bytes',
            'height',
            'width'
        )


class ImagesFieldSerializer(FieldSerializer):

    multi = serializers.BooleanField(
        required=False,
        help_text='Whether to allow multiple image uploads'
    )
    default = serializers.PrimaryKeyRelatedField(
        queryset=models.Image.objects.all(),
        many=True,
        required=False
    )

    class Meta:
        model = models.ImagesField
        fields = FieldSerializer.Meta.fields + (
            'id',
            'multi',
            'default'
        )


class ImagesValueSerializer(ValueSerializer):

    value = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=models.Image.objects.all(),
        required=False
    )
    field = serializers.PrimaryKeyRelatedField(
        queryset=models.ImagesField.objects.all(),
        help_text='Field ID this value belongs to'
    )

    class Meta:
        model = models.ImagesValue
        fields = ValueSerializer.Meta.fields + (
            'id',
            'value',
            'field'
        )


class FileSerializer(serializers.ModelSerializer, TrackTimeSerializer):

    size_bytes = serializers.IntegerField(
        read_only=True,
        help_text='Image size in bytes'
    )

    class Meta:
        model = models.File
        fields = TrackTimeSerializer.Meta.fields + (
            'id',
            'file',
            'size_bytes'
        )


class FileFieldSerializer(FieldSerializer):

    multi = serializers.BooleanField(
        required=False,
        help_text='Whether to allow multiple file uploads'
    )
    default = serializers.PrimaryKeyRelatedField(
        queryset=models.File.objects.all(),
        many=True,
        required=False
    )

    class Meta:
        model = models.FileField
        fields = FieldSerializer.Meta.fields + (
            'id',
            'multi',
            'default'
        )


class FileValueSerializer(ValueSerializer):

    value = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=models.File.objects.all(),
        required=False
    )
    field = serializers.PrimaryKeyRelatedField(
        queryset=models.FileField.objects.all(),
        help_text='Field ID this value belongs to'
    )

    class Meta:
        model = models.FileValue
        fields = ValueSerializer.Meta.fields + (
            'id',
            'value',
            'field'
        )


class ItemFieldSerializer(FieldSerializer):

    multi = serializers.BooleanField(
        required=False,
        help_text='Whether to allow multiple related items'
    )

    default = serializers.PrimaryKeyRelatedField(
        queryset=models.Item.objects.all(),
        many=True,
        required=False
    )

    target_schema = serializers.PrimaryKeyRelatedField(
        queryset=models.ItemSchema.objects.all(),
        required=False,
        allow_null=True,
    )

    class Meta:
        model = models.ItemField
        fields = FieldSerializer.Meta.fields + (
            'id',
            'multi',
            'default',
            'target_schema'
        )


class ItemValueSerializer(ValueSerializer):

    value = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=models.Item.objects.all(),
        required=False
    )
    field = serializers.PrimaryKeyRelatedField(
        queryset=models.ItemField.objects.all(),
        help_text='Field ID this value belongs to'
    )

    class Meta:
        model = models.ItemValue
        fields = ValueSerializer.Meta.fields + (
            'id',
            'value',
            'field'
        )


class CategorySerializer(MaskFieldSerializer, TrackTimeSerializer):
    name = serializers.CharField(
        help_text='Category name'
    )
    description = serializers.CharField(
        help_text='Category description',
        required=False,
        allow_blank=True
    )
    parent = serializers.PrimaryKeyRelatedField(
        queryset=models.Category.objects.all(),
        required=False,
        allow_null=True,
        help_text='Parent category ID'
    )

    class Meta:
        model = models.Category
        fields = TrackTimeSerializer.Meta.fields + (
            'id',
            'name',
            'description',
            'parent'
        )


class ItemSchemaSerializer(MaskFieldSerializer, TrackTimeSerializer):

    name = serializers.CharField(
        help_text='Schema name'
    )

    category = serializers.PrimaryKeyRelatedField(
        queryset=models.Category.objects.all(),
        required=False,
        allow_null=True,
        help_text='Schema category ID'
    )

    image = serializers.PrimaryKeyRelatedField(
        queryset=models.Image.objects.all(),
        required=False,
        allow_null=True,
        help_text='Schema image'
    )
    items_count = serializers.IntegerField(
        read_only=True,
        help_text='Number of items that belongs to this schema'
    )

    config = JSONField(required=False)

    boolean_fields = serializers.PrimaryKeyRelatedField(
        many=True,
        read_only=True,
        help_text='List of boolean fields of this schema'
    )
    choices_fields = serializers.PrimaryKeyRelatedField(
        many=True,
        read_only=True,
        help_text='List of choices fields of this schema'
    )
    datetime_fields = serializers.PrimaryKeyRelatedField(
        many=True,
        read_only=True,
        help_text='List of datetime fields of this schema'
    )
    file_fields = serializers.PrimaryKeyRelatedField(
        many=True,
        read_only=True,
        help_text='List of file fields of this schema'
    )
    images_fields = serializers.PrimaryKeyRelatedField(
        many=True,
        read_only=True,
        help_text='List of images fields of this schema'
    )
    item_fields = serializers.PrimaryKeyRelatedField(
        many=True,
        read_only=True,
        help_text='List of item fields of this schema'
    )
    number_fields = serializers.PrimaryKeyRelatedField(
        many=True,
        read_only=True,
        help_text='List of number fields of this schema'
    )
    text_fields = serializers.PrimaryKeyRelatedField(
        many=True,
        read_only=True,
        help_text='List of text fields of this schema'
    )

    class Meta:
        model = models.ItemSchema
        fields = TrackTimeSerializer.Meta.fields + (
            'id',
            'name',
            'category',
            'image',
            'config',
            'items_count',
            'boolean_fields',
            'choices_fields',
            'datetime_fields',
            'file_fields',
            'images_fields',
            'item_fields',
            'number_fields',
            'text_fields',
        )


class ItemSerializer(MaskFieldSerializer, TrackTimeSerializer):

    schema = serializers.PrimaryKeyRelatedField(
        queryset=models.ItemSchema.objects.all(),
        help_text='Item schema ID'
    )

    boolean_values = serializers.PrimaryKeyRelatedField(
        many=True,
        read_only=True,
        help_text='List of boolean values of this schema'
    )
    choices_values = serializers.PrimaryKeyRelatedField(
        many=True,
        read_only=True,
        help_text='List of choices values of this schema'
    )
    datetime_values = serializers.PrimaryKeyRelatedField(
        many=True,
        read_only=True,
        help_text='List of datetime values of this schema'
    )
    file_values = serializers.PrimaryKeyRelatedField(
        many=True,
        read_only=True,
        help_text='List of file values of this schema'
    )
    images_values = serializers.PrimaryKeyRelatedField(
        many=True,
        read_only=True,
        help_text='List of images values of this schema'
    )
    item_values = serializers.PrimaryKeyRelatedField(
        many=True,
        read_only=True,
        help_text='List of item values of this schema'
    )
    number_values = serializers.PrimaryKeyRelatedField(
        many=True,
        read_only=True,
        help_text='List of number values of this schema'
    )
    text_values = serializers.PrimaryKeyRelatedField(
        many=True,
        read_only=True,
        help_text='List of text values of this schema'
    )

    class Meta:
        model = models.Item
        fields = TrackTimeSerializer.Meta.fields + (
            'id',
            'schema',
            'boolean_values',
            'choices_values',
            'datetime_values',
            'file_values',
            'images_values',
            'item_values',
            'number_values',
            'text_values',
        )


class FieldFilterSerializer(serializers.Serializer):
    item_schema_id__in = serializers.ListSerializer(
        child=serializers.IntegerField(),
        required=False
    )


class ValueFilterSerializer(serializers.Serializer):
    item_id__in = serializers.ListSerializer(
        child=serializers.IntegerField(),
        required=False
    )


class ChoiceFilterSerializer(serializers.Serializer):
    field_id__in = serializers.ListSerializer(
        child=serializers.IntegerField(),
        required=False
    )
    field__item_schema_id__in = serializers.ListSerializer(
        child=serializers.IntegerField(),
        required=False
    )


class ItemFilterSerializer(serializers.Serializer):

    order_by = serializers.CharField(required=False)

    schema_id = serializers.IntegerField(required=False)

    schema__in = serializers.ListSerializer(
        child=serializers.IntegerField(),
        required=False
    )

    created_at__lte = serializers.DateTimeField(required=False)

    created_at__gte = serializers.DateTimeField(required=False)


class ItemSchemaFilterSerializer(serializers.Serializer):

    order_by = serializers.ChoiceField(
        required=False,
        choices=[
            'name',
            'category',
            'created_at',
            'updated_at',
            '-name',
            '-category',
            '-created_at',
            '-updated_at'
        ]
    )

    name__icontains = serializers.CharField(required=False)

    category_id__in = serializers.ListSerializer(
        child=serializers.IntegerField(),
        required=False
    )

    created_at__lte = serializers.DateTimeField(required=False)

    created_at__gte = serializers.DateTimeField(required=False)


class ImportSerializer(serializers.Serializer):
    file = serializers.FileField()
