from django.contrib import admin
from .models import *


@admin.action(description='Create a new academic year')
def create_new_academic_year(modeladmin, request, queryset):
    """
    Admin action to create a new academic year and update the related models.
    """
    # Get the current academic year
    current_academic_year = AnneeScolaire.objects.filter(current=True).first()

    # Create a new academic year
    new_academic_year = AnneeScolaire.objects.create(annee=current_academic_year.annee + 1, current=True)

    # Update the current flag for the previous academic year
    if current_academic_year:
        current_academic_year.current = False
        current_academic_year.save()

    # Create new Niveau and Semestre instances for the new academic year
    for niveau in Niveau.objects.filter(annee_scolaire=current_academic_year):
        new_niveau = Niveau.objects.create(
            annee_scolaire=new_academic_year,
            nom_niveau=niveau.nom_niveau
        )
        for semestre in Semestre.objects.filter(niveau=niveau):
            new_semestre = Semestre.objects.create(
                niveau=new_niveau,
                nom_semestre=semestre.nom_semestre,
                order=semestre.order
            )

    # Update the Questionnaire instances for the new academic year
    for questionnaire in Questionnaire.objects.filter(semester__niveau__annee_scolaire=current_academic_year):
        questionnaire.semester.niveau.annee_scolaire = new_academic_year
        questionnaire.semester.niveau.save()
        questionnaire.semester.save()
        questionnaire.save()

    modeladmin.message_user(request, f"Successfully created a new academic year: {new_academic_year.annee}")




@admin.register(AnneeScolaire)
class AnneeScolaireAdmin(admin.ModelAdmin):
    list_display = ('annee', 'current')
    actions = [create_new_academic_year]

admin.site.register(Questionnaire)
admin.site.register(Semestre)
admin.site.register(Section)
admin.site.register(Question)
admin.site.register(Niveau)
admin.site.register(Datainserted)
admin.site.register(Etudiant)
admin.site.register(Proffesseur)
admin.site.register(Matier)
admin.site.register(Emailtable)
admin.site.register(Studentinfo)
admin.site.register(Specialite)


