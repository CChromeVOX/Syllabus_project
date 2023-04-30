from django.shortcuts import redirect, render
from django.shortcuts import render
from django.urls import reverse
from syllabuses.models import Syllabus, Literature, LiteratureInSyllabus
from .forms import SyllabusForm, SecondStepForm
from django.http import HttpResponseRedirect, JsonResponse

# Create your views here.
def home(request):
    return render(request, 'syllabuses/home.html', {})

def create_syllabus(request):
    if request.method == 'POST':
        form = SyllabusForm(request.POST)
        if form.is_valid():
            syllabus = form.save() 
            return redirect(f'literature_form/{syllabus.id}')
            
    else:
        form = SyllabusForm()
    return render(request, 'syllabuses/create_syllabus.html', {'form': form})


def next_step(request, syllabus_id: int):
    syllabus = Syllabus.objects.get(pk=syllabus_id)
    if request.method == "POST":
        l = request.POST["liter"]
        literature = Literature.objects.get(pk=l)
        mandatory = request.POST["mandatory"]
        LiteratureInSyllabus.objects.create(
            syllabus = syllabus,
            literature = literature,
            mandatory = mandatory
        )
    return render(request, 'syllabuses/next_step.html',{
                      'syllabus': syllabus, 
                      'literatures': Literature.objects.filter(course=syllabus.course),
                      'literaturesinsyllabus': LiteratureInSyllabus.objects.filter(syllabus = syllabus)
                    })

def delete_literature(request, pk, syllabus_id):
    literature = LiteratureInSyllabus.objects.get(pk=pk)
    syllabus_id=syllabus_id
    literature.delete()
    return redirect(f'../../../next_step/{syllabus_id}')

def add_literature(request, syllabus_id: int):
    syllabus = Syllabus.objects.get(pk=syllabus_id)
    # literature_form = SecondStepForm()
    if request.method == "POST":
        title = request.POST["title"]
        Literature.objects.create(
            course=syllabus.course,
            title=title,
        )


    return render(request, 'syllabuses/literature_form.html', 
                  {
                      'syllabus': syllabus, 
                      'literatures': Literature.objects.filter(course=syllabus.course),
                    })