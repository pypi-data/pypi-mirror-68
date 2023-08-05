from rest_framework.routers import SimpleRouter
from django.urls import path

from . import views

app_name = 'drf_schemas'

router = SimpleRouter()

router.register(r'boolean-fields', views.BooleanFieldView, 'boolean-fields')
router.register(r'choices-fields', views.ChoicesFieldView, 'choices-fields')
router.register(r'datetime-fields', views.DateTimeFieldView, 'datetime-fields')
router.register(r'file-fields', views.FileFieldView, 'file-fields')
router.register(r'images-fields', views.ImagesFieldView, 'images-fields')
router.register(r'item-fields', views.ItemFieldView, 'item-fields')
router.register(r'number-fields', views.NumberFieldView, 'number-fields')
router.register(r'text-fields', views.TextFieldView, 'text-fields')

router.register(r'boolean-values', views.BooleanValueView, 'bool-values')
router.register(r'choices-values', views.ChoicesValueView, 'choices-values')
router.register(r'datetime-values', views.DateTimeValueView, 'datetime-values')
router.register(r'file-values', views.FileValueView, 'file-values')
router.register(r'images-values', views.ImagesValueView, 'images-values')
router.register(r'item-values', views.ItemValueView, 'item-values')
router.register(r'number-values', views.NumberValueView, 'number-values')
router.register(r'text-values', views.TextValueView, 'text-values')

router.register(r'choices', views.ChoiceView, 'choices')
router.register(r'files', views.FileView, 'files')
router.register(r'images', views.ImageView, 'images')

router.register(r'categories', views.CategoryView, 'categories')
router.register(r'item-schemas', views.ItemSchemaView, 'item-schemas')
router.register(r'items', views.ItemView, 'items')

urlpatterns = router.urls + [
    path('export/', views.ExportView.as_view(), name='export'),
    path('import/', views.ImportView.as_view(), name='import')
]
