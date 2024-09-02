# document_processor/views.py

from django.shortcuts import render, redirect, get_object_or_404
from .forms import DocumentForm
from .models import Document, ProcessedText
import pytesseract
from PIL import Image
import spacy
from transformers import pipeline
from pdf2image import convert_from_path

# Tesseract path (if necessary)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

nlp = spacy.load("en_core_web_sm")
text_classifier = pipeline("text-classification")
sentiment_analyzer = pipeline("sentiment-analysis")



def upload_document(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save()
            process_document(document)
            return redirect('document_list')
    else:
        form = DocumentForm()
    return render(request, 'document_processor/upload.html', {'form': form})

def process_document(document):
    if document.file.path.endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif')):
        image = Image.open(document.file.path)
        languages = 'eng+hin'
        extracted_text = pytesseract.image_to_string(image, lang=languages)
    elif document.file.path.endswith('.pdf'):
        extracted_text = handle_pdf(document.file.path, languages='eng+hin')
    else:
        extracted_text = "Unsupported file format."

    document.extracted_text = extracted_text
    document.save()

    ai_process_document(document)

def ai_process_document(document):
    doc = nlp(document.extracted_text)
    entities = [(ent.text, ent.label_) for ent in doc.ents]
    document.named_entities = entities

    text_classification = text_classifier(document.extracted_text[:512])
    document.text_classification = text_classification

    sentiment = sentiment_analyzer(document.extracted_text[:512])
    document.sentiment = sentiment

    document.save()

def handle_pdf(pdf_path, languages='eng+hin'):
    images = convert_from_path(pdf_path)
    extracted_text = ''
    for image in images:
        extracted_text += pytesseract.image_to_string(image, lang=languages)
    return extracted_text

def document_list(request):
    documents = Document.objects.all()
    return render(request, 'document_processor/document_list.html', {'documents': documents})

def processed_text(request, pk):
    document = get_object_or_404(Document, pk=pk)
    processed_text = get_object_or_404(ProcessedText, document=document)
    return render(request, 'document_processor/processed_text.html', {'document': document, 'processed_text': processed_text})
