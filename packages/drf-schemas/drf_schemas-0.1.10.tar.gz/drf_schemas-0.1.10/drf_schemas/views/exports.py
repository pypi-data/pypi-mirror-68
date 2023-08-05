import json
from datetime import datetime

from django.http import HttpResponse
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from ..serializers import ImportSerializer
from ..services import export_schemas, import_schemas

JSON_MIME = 'application/json'
JSON_NAME = 'attachment; filename="schemas-{}.json"'


class ExportView(APIView):

    def get(self, request):
        params = self.request.query_params

        now = datetime.now().strftime('%Y%m%d-%H%M')
        response = HttpResponse(content_type=JSON_MIME)
        response['Content-Disposition'] = JSON_NAME.format(now)

        data = export_schemas()
        json.dump(data, response)

        return response


class ImportView(APIView):

    def post(self, request):
        serializer = ImportSerializer(
            data=request.data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        file = serializer.validated_data['file']
        try:
            data = json.load(file)
        except Exception as error:
            raise ValidationError(error)
        else:
            errors = import_schemas(data)
            if errors:
                raise ValidationError(errors)

        return Response(status=status.HTTP_201_CREATED)
