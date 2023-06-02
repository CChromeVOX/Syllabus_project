from django.shortcuts import redirect, render
from django.shortcuts import render
from django.urls import reverse
from syllabuses.models import *
from .forms import *
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404

# Create your views here.
def home(request):
    return render(request, 'syllabuses/home.html', {})



def login_v(request): 
    if request.method == 'POST': 
        form = AuthenticationForm(data=request.POST) 
        if form.is_valid(): 
            username = form.cleaned_data.get('username') 
            password = form.cleaned_data.get('password') 
            user = authenticate(request, username=username, password=password) 
            if user is not None: 
                login(request, user) 
                return redirect('../create_syllabus') 
            else: 
                print(request, "Why is this not returned for inval")       
    else: 
        form = AuthenticationForm() 
    return render(request, 'syllabuses/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('../create_syllabus')


























def create_syllabus(request):
    if request.method == 'POST':
        form = SyllabusForm(request.POST)
        if form.is_valid():
            syllabus.status = Status.objects.get(type="Created")
            syllabus = form.save() 
            return redirect(f'literature_form/{syllabus.id}')
            
    else:
        form = SyllabusForm()
    return render(request, 'syllabuses/create_syllabus.html', {'form': form})


def next_step(request, syllabus_id: int):
    syllabus = Syllabus.objects.get(pk=syllabus_id)
    if request.method == "POST":
        syllabus.status = Status.objects.get(type="added literature")
        syllabus.save()
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


def delete_syllabus(request, syllabus_id):
    syl = Syllabus.objects.get(pk=syllabus_id)
    syl.delete()
    return redirect(f'../../../my_syllabuses')

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



def syllabus_details(request, syllabus_id: int):
    syllabus = get_object_or_404(Syllabus, pk=syllabus_id)
    lo11 = CourseLO.objects.filter(syllabus=syllabus).filter(type=True)
    lo22 = CourseLO.objects.filter(syllabus=syllabus).filter(type=False)
    modules = Module.objects.filter(syllabus=syllabus).order_by('week')

    if request.method == 'POST':
        syllabus.syllabus_name= request.POST.get('syllabus_name')
        course = request.POST.get('course')
        training_level = request.POST.get('training_level')
        language_of_education = request.POST.get('language_of_education')
        proficiency_level = request.POST.get('proficiency_level')
        total_hours = request.POST.get('total_hours')
        classroom_hours = request.POST.get('classroom_hours')
        semester = request.POST.get('semester')
        ects = request.POST.get('ects')
        iw_hours = request.POST.get('iw_hours')
        prerequisites = request.POST.get('prerequisites')
        format_of_training = request.POST.get('format_of_training')
        edu_programms = request.POST.get('edu_programms')
        time_place = request.POST.get('time_place')
        instructor = request.POST.get('instructor')
        course_objective = request.POST.get('course_objective')
        agreed_with = request.POST.get('agreed_with')
        status = request.POST.get('status')
        course_philosophy = request.POST.get('course_philosophy')
        course_etics = request.POST.get('course_etics')
        asu = request.POST.get('asu')
        syllabus.course = Course.objects.get(pk=course)
        syllabus.training_level = EduLevel.objects.get(pk=training_level)
        syllabus.language_of_education = Language.objects.get(pk=language_of_education)
        syllabus.proficiency_level = Proficiency.objects.get(pk=proficiency_level)
        syllabus.total_hours = total_hours
        syllabus.classroom_hours = classroom_hours
        syllabus.semester = semester
        syllabus.ects = ects
        syllabus.iw_hours = iw_hours
        syllabus.prerequisites = prerequisites
        syllabus.format_of_training = Format.objects.get(pk=format_of_training)
        syllabus.edu_programms = edu_programms
        syllabus.time_place = time_place
        syllabus.instructor = CustomUser.objects.get(pk=instructor)
        syllabus.course_objective = course_objective
        syllabus.agreed_with = Director.objects.get(pk=agreed_with)
        syllabus.status = Status.objects.get(pk=status)
        syllabus.course_philosophy = course_philosophy
        syllabus.course_etics = course_etics
        if asu=="on":
            syllabus.asu = True
        else: 
            syllabus.asu = False
        syllabus.save()
        return redirect(reverse('syllabus_details', args=[syllabus_id]))
    
    
    return render(request, 'syllabuses/syllabus_details.html', {
        'syllabus': syllabus,
        'literatures': LiteratureInSyllabus.objects.filter(syllabus=syllabus),
        'lo11': lo11,
        'lo22': lo22,
        'modules': modules,
        'courses': Course.objects.all(),
        'edu_levels': EduLevel.objects.all(),
        'languages': Language.objects.all(),
        'proficiencies': Proficiency.objects.all(),
        'formats': Format.objects.all(),
        'instructors': CustomUser.objects.all(),
        'directors': Director.objects.all(),
        'statuses': Status.objects.all(),
    })





def half(request, syllabus_id: int):
    syllabus = Syllabus.objects.get(pk=syllabus_id)
  # literature_form = SecondStepForm()
    if request.method == "POST":
        syllabus.status = Status.objects.get(type="added lo")
        syllabus.save()
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

def edit_profile(request):
    currentuser = request.user

    return render(request, 'syllabuses/edit_profile.html', 
                  {
                      'user': currentuser, 

                    })


def add_policy(request, syllabus_id: int):
    syllabus = Syllabus.objects.get(pk=syllabus_id)
    if request.method == "POST":
        syllabus.status = Status.objects.get(type="added policy")
        syllabus.course_philosophy = request.POST["phylosophy"]
        syllabus.course_etics = request.POST["policy"]
        syllabus.save()

    return render(request, 'syllabuses/add_policy.html', 
                  {
                      'syllabus': syllabus, 
                    })



def add_module(request, syllabus_id: int):
    syllabus = Syllabus.objects.get(pk=syllabus_id)

    if request.method == "POST":
        syllabus.status = Status.objects.get(type="added modules")
        syllabus.save()
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



def continue_edit(request, syllabus_id: int):
    syllabus = Syllabus.objects.get(pk=syllabus_id)
    print(syllabus.status)

    if syllabus.status == Status.objects.get(type="Created"):
        return redirect(f'../../literature_form/{syllabus_id}')
    elif syllabus.status == Status.objects.get(type="added literature"):
        return redirect(f'../../half/{syllabus_id}')
    elif syllabus.status == Status.objects.get(type="added lo"):
        return redirect(f'../../add_module/{syllabus_id}')
    else: return redirect(reverse('syllabus_details', args=[syllabus_id]))






def my_syllabuses(request):
    syllabuses = Syllabus.objects.filter(instructor=request.user)

    return render(request, 'syllabuses/my_syllabuses.html', 
                  {
                      'syllabuses': syllabuses, 
                    })

