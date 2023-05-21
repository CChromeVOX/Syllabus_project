from django.shortcuts import redirect, render
from django.shortcuts import render
from django.urls import reverse
from syllabuses.models import Syllabus, Literature, LiteratureInSyllabus, Module, Format, CourseLO
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

def delete_module(request, pk, syllabus_id):
    module = Module.objects.get(pk=pk)
    syllabus_id=syllabus_id
    module.delete()
    return redirect(f'../../../add_module/{syllabus_id}')

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


def half(request, syllabus_id: int):
    syllabus = Syllabus.objects.get(pk=syllabus_id)
  # literature_form = SecondStepForm()
    if request.method == "POST":
        lo = request.POST["lo"]
        lo2 = request.POST["lo2"]
        CourseLO.objects.create(
            syllabus=syllabus,
            type = True,
            info = lo
        )
        CourseLO.objects.create(
            syllabus=syllabus,
            type = False,
            info = lo2
        )


    return render(request, 'syllabuses/half.html', 
                  {
                      'syllabus': syllabus, 

                    })


def add_module(request, syllabus_id: int):
    syllabus = Syllabus.objects.get(pk=syllabus_id)

    if request.method == "POST":
        week = request.POST["week"]
        theme = request.POST["theme"]
        format = Format.objects.get(pk = request.POST["format"]) 
        tasks = request.POST["tasks"]
        lo = request.POST["lo"]
        questions = request.POST["questions"]
        liter = LiteratureInSyllabus.objects.get(pk = request.POST["liter"]) 
        grading = request.POST["grading"]
        maxpercent = request.POST["maxpercent"]
        maxvalue = request.POST["maxvalue"]
        total_in_points = request.POST["total_in_points"]

        Module.objects.create(
            syllabus=syllabus,
            week=week,
            tasks=tasks,
            course_lo=lo,
            theme=theme,
            format=format,
            questions=questions,
            literature=liter,
            grading=grading,
            max_percent=maxpercent,
            max_weight=maxvalue,
            total_in_points=total_in_points,
        )


    return render(request, 'syllabuses/add_module.html', 
                  {
                      'syllabus': syllabus, 
                      'literatures': LiteratureInSyllabus.objects.filter(syllabus=syllabus),
                      'formats': Format.objects.all(),
                      'modules': Module.objects.filter(syllabus=syllabus).order_by('week'),
                      'lo11': CourseLO.objects.get(syllabus=syllabus, type=True),
                      'lo22': CourseLO.objects.get(syllabus=syllabus, type=False),
                    })