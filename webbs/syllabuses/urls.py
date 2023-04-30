from django.urls import path
from . import views
urlpatterns = [
    path('', views.home, name="home"),
    path('create_syllabus', views.create_syllabus, name="create_syllabus"),
    path('literature_form/<int:syllabus_id>', views.add_literature, name="literature_form"),
    path('literature/delete/<int:pk>/<int:syllabus_id>', views.delete_literature, name='delete_literature'),
    path('next_step/<int:syllabus_id>', views.next_step, name="next_step"),
    
]