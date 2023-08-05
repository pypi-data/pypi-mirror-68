from threading import Thread

from django.db.models import QuerySet

from . import models
from . import serializers
from . import resources
import tablib
from import_export.resources import modelresource_factory

_field_params = [{
    'fields': 'boolean_fields',
    'values': 'boolean_values',
    'value_model': models.BooleanValue,
    'field_model': models.BooleanField,
    'field_serializer': serializers.BooleanFieldSerializer,
    'value_serializer': serializers.BooleanValueSerializer,
}, {
    'fields': 'choices_fields',
    'values': 'choices_values',
    'value_model': models.ChoicesValue,
    'field_model': models.ChoicesField,
    'field_serializer': serializers.ChoicesFieldSerializer,
    'value_serializer': serializers.ChoicesValueSerializer,
}, {
    'fields': 'datetime_fields',
    'values': 'datetime_values',
    'value_model': models.DateTimeValue,
    'field_model': models.DateTimeField,
    'field_serializer': serializers.DateTimeFieldSerializer,
    'value_serializer': serializers.DateTimeValueSerializer,
}, {
    'fields': 'number_fields',
    'values': 'number_values',
    'value_model': models.NumberValue,
    'field_model': models.NumberField,
    'field_serializer': serializers.NumberFieldSerializer,
    'value_serializer': serializers.NumberValueSerializer,
}, {
    'fields': 'images_fields',
    'values': 'images_values',
    'value_model': models.ImagesValue,
    'field_model': models.ImagesField,
    'field_serializer': serializers.ImagesFieldSerializer,
    'value_serializer': serializers.ImagesValueSerializer,
}, {
    'fields': 'file_fields',
    'values': 'file_values',
    'value_model': models.FileValue,
    'field_model': models.FileField,
    'field_serializer': serializers.FileFieldSerializer,
    'value_serializer': serializers.FileValueSerializer,
}, {
    'fields': 'text_fields',
    'values': 'text_values',
    'value_model': models.TextValue,
    'field_model': models.TextField,
    'field_serializer': serializers.TextFieldSerializer,
    'value_serializer': serializers.TextValueSerializer,
}, {
    'fields': 'item_fields',
    'values': 'item_values',
    'value_model': models.ItemValue,
    'field_model': models.ItemField,
    'field_serializer': serializers.ItemFieldSerializer,
    'value_serializer': serializers.ItemValueSerializer,
}]

_multi_values = (
    'choices_values',
    'item_values',
    'images_values',
    'file_values'
)


def update_item(item: models.Item = None):

    if item is None:
        return

    schema = item.schema

    for param in _field_params:

        fields_queryset = getattr(schema, param['fields']).all()
        values_queryset = getattr(item, param['values']).all()

        if len(fields_queryset) or len(values_queryset):
            fields = {field.pk: field for field in fields_queryset}
            values = {value.field.pk: value for value in values_queryset}

            fields_pk = set(fields)
            values_pk = set(values)

            create_pk = fields_pk - values_pk
            delete_pk = values_pk - fields_pk

            value_model = param['value_model']

            for pk in create_pk:
                field = fields[pk]
                if param['values'] in _multi_values:
                    value = value_model.objects.create(
                        item=item,
                        field=field
                    )
                    default = field.default.all()
                    if len(default):
                        value.value.set(default)
                else:
                    value_model.objects.create(
                        item=item,
                        field=field,
                        value=field.default
                    )

            for pk in delete_pk:
                values[pk].delete()


class ItemUpdater(Thread):

    def __init__(self, queryset: QuerySet, daemon: bool = True):
        super().__init__(daemon=daemon)
        self.queryset = queryset

    def run(self):
        for item in self.queryset.iterator():
            update_item(item)


_ie_resources = [{
    'name': 'categories',
    'resource': resources.CategoryResource,
    'model': models.Category
}, {
    'name': 'item_schemas',
    'resource': resources.ItemSchemaResource,
    'model': models.ItemSchema
}, {
    'name': 'boolean_fields',
    'resource': resources.BooleanFieldResource,
    'model': models.BooleanField
}, {
    'name': 'choices_fields',
    'resource': resources.ChoicesFieldResource,
    'model': models.ChoicesField
}, {
    'name': 'datetime_fields',
    'resource': resources.DateTimeFieldResource,
    'model': models.DateTimeField
}, {
    'name': 'file_fields',
    'resource': resources.FileFieldResource,
    'model': models.FileField
}, {
    'name': 'images_fields',
    'resource': resources.ImagesFieldResource,
    'model': models.ImagesField
}, {
    'name': 'item_fields',
    'resource': resources.ItemFieldResource,
    'model': models.ItemField
}, {
    'name': 'number_fields',
    'resource': resources.NumberFieldResource,
    'model': models.NumberField
}, {
    'name': 'text_fields',
    'resource': resources.TextFieldResources,
    'model': models.TextField
}, {
    'name': 'choices',
    'resource': resources.ChoiceResource,
    'model': models.Choice
}]


def export_schemas(output: str = 'dict'):
    data = {}
    for param in _ie_resources:
        dataset = param['resource']().export()
        data[param['name']] = getattr(dataset, output)

    return data


def import_schemas(data: dict):
    for param in _ie_resources:
        model_resource = modelresource_factory(model=param['model'])()
        dataset = tablib.Dataset()
        dataset.dict = data[param['name']]
        result = model_resource.import_data(dataset, dry_run=True)
        if result.has_errors():
            row_errors = result.row_errors()
            row_errors = {
                row_error[0]: [error_obj.error for error_obj in row_error[1]]
                for row_error in row_errors
            }

            base_errors = result.base_errors
            base_errors = [error_obj.error for error_obj in base_errors]

            return {
                param['name']: {
                    'base_errors': base_errors,
                    'row_errors': row_errors
                }
            }

        model_resource.import_data(dataset, dry_run=False)


# def export_schemas(context: [dict, None] = None):
#     data = {}
#     for param in _schema_params:
#         serializer = param['serializer'](
#             param['model'].objects.all(),
#             context=context,
#             many=True
#         )
#         data[param['name']] = serializer.data
#
#     for name, values in _init_fields.items():
#         for field, value in values.items():
#             for item in data[name]:
#                 item[field] = value
#
#     return data
