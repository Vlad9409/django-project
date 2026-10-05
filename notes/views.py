from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .models import Note, Category
from .forms import NoteForm


# Create your views here.

@login_required(login_url='login')
def home_text(request):
    # Замість Note.objects.all() беремо нотатки ТІЛЬКИ поточного юзера
    notes_data = Note.objects.filter(user=request.user)
    categories = Category.objects.all()

    # Далі ваш звичайний код пошуку та фільтрації, він працює з notes_data
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


@login_required(login_url='login')
def note_create(request):
    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False) # Зупиняємо збереження
            note.user = request.user       # Прикріплюємо поточного юзера
            note.save()                    # Тепер зберігаємо в базу
            return redirect('home_text')
    else:
        form = NoteForm()

    return render(request, 'notes/note_form.html', {'form': form, 'action_title': 'Створити нотатку'})


@login_required(login_url='login')
def note_edit(request, pk):
    # Додаємо user=request.user, щоб ніхто не міг редагувати чужі нотатки, ввівши їхній ID в URL
    note = get_object_or_404(Note, pk=pk, user=request.user)

    if request.method == 'POST':
        form = NoteForm(request.POST, instance=note)
        if form.is_valid():
            form.save()
            return redirect('home_text')
    else:
        form = NoteForm(instance=note)

    return render(request, 'notes/note_form.html', {'form': form, 'action_title': 'Редагувати нотатку', 'note': note})


@login_required(login_url='login')
def note_delete(request, pk):
    # Аналогічно захищаємо видалення
    note = get_object_or_404(Note, pk=pk, user=request.user)

    if request.method == 'POST':
        note.delete()
        return redirect('home_text')

    return render(request, 'notes/note_confirm_delete.html', {'note': note})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home_text')
    else:
        form = AuthenticationForm()
    
    return render(request, 'registration/login.html', {'form': form})

def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home_text')