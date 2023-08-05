from django.core.exceptions import ObjectDoesNotExist
from django.http import QueryDict
from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.response import Response


class RetrieveMixin:

    # noinspection PyUnresolvedReferences
    def retrieve(self, request, pk):
        serializer_context = {'request': request}
        try:
            pk = int(pk)
            instance = self.queryset.get(pk=pk)
        except (ObjectDoesNotExist, ValueError):
            raise NotFound(f'A {self.model_name} with pk={pk} does not exist.')

        serializer = self.serializer_class(
            instance,
            context=serializer_context
        )
        return Response(serializer.data, status=status.HTTP_200_OK)


class ListMixin:

    # noinspection PyUnresolvedReferences
    def list(self, request):
        serializer_context = {'request': request}
        page = self.paginate_queryset(self.get_queryset())

        fields = request.query_params.get('fields', None)
        if fields is not None:
            fields = fields.split(',')

        serializer = self.serializer_class(
            page,
            context=serializer_context,
            many=True,
            fields=fields
        )
        return self.get_paginated_response(serializer.data)


class CreateMixin:

    # noinspection PyUnresolvedReferences
    def create(self, request):
        serializer_context = {'request': request}
        serializer = self.serializer_class(
            data=request.data,
            context=serializer_context
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        serializer = self.serializer_class(
            serializer.instance,
            context=serializer_context
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UpdateMixin:

    # noinspection PyUnresolvedReferences
    def partial_update(self, request, pk=None):
        try:
            pk = int(pk)
            instance = self.queryset.get(pk=pk)
        except (ObjectDoesNotExist, ValueError):
            raise NotFound(f'A {self.model_name} with pk={pk} does not exist.')

        serializer_context = {'request': request}
        serializer = self.serializer_class(
            instance,
            data=request.data,
            context=serializer_context,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        serializer = self.serializer_class(
            serializer.instance,
            context=serializer_context
        )
        return Response(serializer.data, status=status.HTTP_200_OK)


class DestroyMixin:

    # noinspection PyUnresolvedReferences
    def destroy(self, request, pk=None):
        try:
            pk = int(pk)
            instance = self.queryset.get(pk=pk)
        except (ObjectDoesNotExist, ValueError):
            raise NotFound(f'A {self.model_name} with pk={pk} does not exist.')

        instance.delete()

        return Response(None, status=status.HTTP_204_NO_CONTENT)


# noinspection PyUnresolvedReferences
class FilterMixin:

    multi_query = ()

    def get_queryset(self):
        queryset = self.queryset
        params: QueryDict = self.request.query_params

        if len(params):
            params = params.lists()
            data = {
                key: value if key in self.multi_query else value[0]
                for key, value in params
            }
            serializer_class = self.filter_serializer_class
            serializer = serializer_class(
                data=data,
                context={'request': self.request}
            )
            serializer.is_valid(raise_exception=True)

            params = serializer.data
            order_by = params.pop('order_by', '')
            queryset = queryset.filter(**params)

            if order_by:
                queryset = queryset.order_by(order_by)

        return queryset
