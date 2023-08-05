from rest_framework import viewsets

from ._mixins import (
    CreateMixin,
    ListMixin,
    RetrieveMixin,
    DestroyMixin,
    UpdateMixin,
    FilterMixin
)
from ..models import (
    DateTimeField,
    NumberField,
    TextField,
    BooleanField,
    ChoicesField,
    ImagesField,
    FileField,
    ItemField
)
from ..serializers import (
    DateTimeFieldSerializer,
    NumberFieldSerializer,
    TextFieldSerializer,
    BooleanFieldSerializer,
    ChoicesFieldSerializer,
    ImagesFieldSerializer,
    FileFieldSerializer,
    ItemFieldSerializer,
    FieldFilterSerializer
)


class FieldView(
    CreateMixin,
    ListMixin,
    RetrieveMixin,
    DestroyMixin,
    UpdateMixin,
    FilterMixin,
    viewsets.GenericViewSet
):

    lookup_field = 'pk'
    multi_query = ('item_schema_id__in',)
    filter_serializer_class = FieldFilterSerializer



class DateTimeFieldView(FieldView):

    model_name = 'DateTimeField'
    queryset = DateTimeField.objects.all()
    serializer_class = DateTimeFieldSerializer


class NumberFieldView(FieldView):

    model_name = 'NumberField'
    queryset = NumberField.objects.all()
    serializer_class = NumberFieldSerializer


class TextFieldView(FieldView):

    model_name = 'TextField'
    queryset = TextField.objects.all()
    serializer_class = TextFieldSerializer


class BooleanFieldView(FieldView):

    model_name = 'BooleanField'
    queryset = BooleanField.objects.all()
    serializer_class = BooleanFieldSerializer


class ChoicesFieldView(FieldView):

    model_name = 'ChoicesField'
    queryset = ChoicesField.objects.all()
    serializer_class = ChoicesFieldSerializer


class ImagesFieldView(FieldView):

    model_name = 'ImagesField'
    queryset = ImagesField.objects.all()
    serializer_class = ImagesFieldSerializer


class FileFieldView(FieldView):

    model_name = 'FileField'
    queryset = FileField.objects.all()
    serializer_class = FileFieldSerializer


class ItemFieldView(FieldView):

    model_name = 'ItemField'
    queryset = ItemField.objects.all()
    serializer_class = ItemFieldSerializer

