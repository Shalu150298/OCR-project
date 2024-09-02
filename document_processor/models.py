# document_processor/models.py

from django.db import models
from django.contrib.auth.models import User

class Document(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    file = models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    extracted_text = models.TextField(blank=True, null=True)
    named_entities = models.JSONField(blank=True, null=True)
    text_classification = models.JSONField(blank=True, null=True)
    sentiment = models.JSONField(blank=True, null=True)

    def __str__(self):
        return self.file.name

class ProcessedText(models.Model):
    document = models.OneToOneField(Document, on_delete=models.CASCADE)
    processed_data = models.JSONField()

    def __str__(self):
        return f"Processed data for {self.document.file.name}"
