from django.urls import path
from . import views
urlpatterns = [
    path('', views.home, name="home"),
    path('create_syllabus', views.create_syllabus, name="create_syllabus"),
    path('literature_form', views.add_literature, name="literature_form"),
    path('next_step', views.next_step, name="next_step"),
    
]