from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Note, Category
from .forms import NoteForm

# Create your views here.

def home_text(request):
    notes_data = Note.objects.all()
    categories = Category.objects.all()

    search_query = request.GET.get('search', '')
    if search_query:
        notes_data = notes_data.filter(title__icontains=search_query)

    category_id = request.GET.get('category', '')
    if category_id:
        notes_data = notes_data.filter(category_id=category_id)

    context = {
        'title': 'My notes',
        'notes': notes_data,
        'categories': categories,
        'search_query': search_query,
        'category_id': int(category_id) if category_id else '',
    }
    return render(request, 'notes/home_text.html', context)

def note_create(request):
    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home_text')
    else:
        form = NoteForm()
    
    return render(request, 'notes/note_form.html', {'form': form, 'action_title': 'Створити нотатку'})


def note_edit(request, pk):
    note = get_object_or_404(Note, pk=pk)
    
    if request.method == 'POST':
        form = NoteForm(request.POST, instance=note)
        if form.is_valid():
            form.save()
            return redirect('home_text')
    else:
        form = NoteForm(instance=note)
        
    return render(request, 'notes/note_form.html', {'form': form, 'action_title': 'Редагувати нотатку', 'note': note})

def note_delete(request, pk):
    note = get_object_or_404(Note, pk=pk)
    if request.method == 'POST':
        note.delete()
        return redirect('home_text')
    return render(request, 'notes/note_confirm_delete.html', {'note': note})