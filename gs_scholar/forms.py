# forms.py

from django import forms
from .models import Questionnaire, Section, Question, Emailtable

class StudentImportForm(forms.Form):
    excel_file = forms.FileField()

class QuestionnaireResponseForm(forms.Form):
    def __init__(self, *args, **kwargs):
        questionnaire_id = kwargs.pop('questionnaire_id')
        super(QuestionnaireResponseForm, self).__init__(*args, **kwargs)

        sections = Section.objects.filter(questionnaire_id=questionnaire_id)

        for section in sections:
            questions = Question.objects.filter(section_id=section.id)
            for question in questions:
                field_name = f"question_{question.id}"
                if question.choices:
                    choices = [choice.strip() for choice in question.choices.split(',')]
                    self.fields[field_name] = forms.ChoiceField(
                        label=question.text,
                        choices=[(choice, choice) for choice in choices],
                        widget=forms.RadioSelect
                    )
                else:
                    self.fields[field_name] = forms.CharField(label=question.text, required=False)



class ImportMatiereForm(forms.Form):
    excel_file = forms.FileField(
        label='Choose a file',
        widget=forms.FileInput(attrs={'class': 'form-control'})
    )


class SectionForm(forms.ModelForm):
    class Meta:
        model = Section
        fields = ['name', 'order']


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['section', 'text', 'choices', 'question_type']

# forms.py
from django import forms
from gs_scholar.models import Semestre, Specialite

class QuestionnaireDispatchForm(forms.Form):
    semesters = forms.ModelMultipleChoiceField(
        queryset=Semestre.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True,
        label="Select Semesters"
    )
    specialties = forms.ModelMultipleChoiceField(
        queryset=Specialite.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Select Specialties (if applicable)"
    )
    include_common = forms.BooleanField(
        required=False, 
        initial=True, 
        label="Include Common Courses"
    )
    expiration_hours = forms.FloatField(
        required=True, 
        initial=24, 
        label="Expiration Time (hours)"
    )





class EmailtableForm(forms.ModelForm):
    class Meta:
        model = Emailtable
        fields = ['email', 'niveau']
