from django import forms
from .models import Literature, Syllabus

class SyllabusForm(forms.ModelForm):
    class Meta:
        model = Syllabus
        fields = [
            'syllabus_name',
            'course',
            'training_level',
            'language_of_education',
            'proficiency_level',
            'total_hours',
            'classroom_hours',
            'semester',
            'ects',
            'iw_hours',
            'prerequisites',
            'format_of_training',
            'edu_programms',
            'time_place',
            'instructor',
            'course_objective',
            'agreed_with',
            'asu',
        ]
        widgets = {
            'prerequisites': forms.Textarea(attrs={'rows': 4}),
            'edu_programms': forms.Textarea(attrs={'rows': 4}),
            'time_place': forms.Textarea(attrs={'rows': 4}),
            'course_objective': forms.Textarea(attrs={'rows': 4}),
        }


class SecondStepForm(forms.ModelForm):
    class Meta:
        model = Literature
        fields = ['course', 'number', 'title']
        labels = {
            'course': 'Дисциплина',
            'number': 'Номер',
            'title': 'Название',
        }

    def __init__(self, *args, **kwargs):
        course = kwargs.pop('course', None)
        super(SecondStepForm, self).__init__(*args, **kwargs)
        if course:
            self.fields['course'].initial = course