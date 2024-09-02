# document_processor/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.upload_document, name='upload_document'),
    path('documents/', views.document_list, name='document_list'),
    path('documents/<int:pk>/', views.processed_text, name='processed_text'),
]
