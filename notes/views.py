from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def home_text(request):
    
    courses_data = [
            {'name' : 'Lear Python', 'price' : 100, 'avaliable' : True},
            {'name' : 'Lear Django', 'price' : 50, 'avaliable' : True},
            {'name' : 'Advance JavaScript', 'price' : 80, 'avaliable' : False},
            {'name' : 'Devops courses', 'price' : 70, 'avaliable' : False},
            {'name' : 'Reacrt advance', 'price' : 90, 'avaliable' : False},
        ]
    
    context = {
        'title' : 'Our courses',
        'courses' : courses_data
    }
    return render(request, 'notes/home_text.html', context)