from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def home_text(request):
    
    notes_data = [
            {'name' : 'Buy a product', 'status' : 'done'},
            {'name' : 'go to gym', 'status' : 'not',},
            {'name' : 'Learn python', 'status' : 'done',},
            {'name' : 'Watch movie', 'status' : 'not',},
            {'name' : 'Go sleep', 'status' : 'not',},
        ]
    
    context = {
        'title' : 'My notes',
        'notes' : notes_data
    }
    return render(request, 'notes/home_text.html', context)