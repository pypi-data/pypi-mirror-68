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
    Item,
    ItemSchema,
    Category
)
from ..serializers import (
    ItemSerializer,
    ItemSchemaSerializer,
    CategorySerializer,
    ItemFilterSerializer,
    ItemSchemaFilterSerializer
)


class ItemView(
    CreateMixin,
    ListMixin,
    RetrieveMixin,
    DestroyMixin,
    UpdateMixin,
    FilterMixin,
    viewsets.GenericViewSet
):

    lookup_field = 'pk'
    model_name = 'Item'
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    multi_query = ('schema__in',)
    filter_serializer_class = ItemFilterSerializer


class CategoryView(
    CreateMixin,
    ListMixin,
    RetrieveMixin,
    DestroyMixin,
    UpdateMixin,
    viewsets.GenericViewSet
):

    lookup_field = 'pk'
    model_name = 'Category'
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_queryset(self):
        queryset = self.queryset

        name = self.request.query_params.get('name', '')
        if name:
            queryset = queryset.filter(name__icontains=name)

        order_by = self.request.query_params.get('order_by', '')
        if order_by in ['name', 'created_at', 'updated_at']:
            queryset = queryset.order_by(order_by)

        return queryset


class ItemSchemaView(ItemView):

    model_name = 'ItemSchema'
    queryset = ItemSchema.objects.all()
    serializer_class = ItemSchemaSerializer
    multi_query = ('category_id__in',)
    filter_serializer_class = ItemSchemaFilterSerializer


