from django.shortcuts import render
from django.http import HttpResponse
from .models import Note

# Create your views here.

def home_text(request):
    
    notes_data = Note.objects.all()

    context = {
        'title': 'My notes',
        'notes': notes_data,
    }
    return render(request, 'notes/home_text.html', context)