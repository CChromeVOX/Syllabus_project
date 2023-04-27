from django.shortcuts import redirect, render
from django.shortcuts import render
from syllabuses.models import Syllabus
from .forms import SyllabusForm, SecondStepForm
from django.http import JsonResponse

# Create your views here.
def home(request):
    return render(request, 'syllabuses/home.html', {})

def create_syllabus(request):
    if request.method == 'POST':
        form = SyllabusForm(request.POST)
        if form.is_valid():
            syllabus = form.save() 
            return redirect('syllabuses/literature_form.html', {'syllabus': syllabus})
            
    else:
        form = SyllabusForm()
    return render(request, 'syllabuses/create_syllabus.html', {'form': form})


def next_step(request):
    return render(request, 'syllabuses/next_step.html', {})


def add_literature(request):

    literature_form = SecondStepForm()
    

    return render(request, 'syllabuses/literature_form.html', {'literature_form': literature_form})