from django.db import models
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class Specialite(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=10, unique=True)  # Ensure code is unique
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.code} - {self.name}"

class AnneeScolaire(models.Model):
    annee = models.IntegerField(unique=True)
    current = models.BooleanField(default=False)

    def __str__(self):
        return str(self.annee)

    def save(self, *args, **kwargs):
        if self.current:
            # Ensure only one AnneeScolaire is current at a time
            AnneeScolaire.objects.exclude(pk=self.pk).update(current=False)
        super().save(*args, **kwargs)

class Niveau(models.Model):
    NIVEAU_CHOICES = [
        ('L1', 'License 1'),
        ('L2', 'License 2'),
        ('L3', 'License 3'),
    ]

    annee_scolaire = models.ForeignKey(AnneeScolaire, on_delete=models.CASCADE)
    nom_niveau = models.CharField(max_length=255, choices=NIVEAU_CHOICES)
    specialite = models.ForeignKey(Specialite, on_delete=models.SET_NULL, null=True, blank=True) # Changed to SET_NULL

    def __str__(self):
        if self.specialite and self.nom_niveau in ['L2', 'L3']:
            return f"{self.nom_niveau} - {self.specialite} - {self.annee_scolaire}"
        return f"{self.nom_niveau} - {self.annee_scolaire}"

    def clean(self):
        # Validation to ensure L1 doesn't have a specialite, but L2/L3 *must* have one.
        if self.nom_niveau == 'L1' and self.specialite:
            raise ValidationError({'specialite': "L1 cannot have a specialty."})
        elif self.nom_niveau in ['L2', 'L3'] and not self.specialite:
            raise ValidationError({'specialite': "L2 and L3 must have a specialty."})

    def save(self, *args, **kwargs):
        self.full_clean()  # Ensure clean() is called before saving
        super().save(*args, **kwargs)

@receiver(post_save, sender=AnneeScolaire)
def update_niveaux_on_annee_change(sender, instance, **kwargs):
    if instance.current:  # Only act if the AnneeScolaire is set to current
        Niveau.objects.filter(annee_scolaire=instance).update(annee_scolaire=instance)

class Semestre(models.Model):
    niveau = models.ForeignKey(Niveau, on_delete=models.CASCADE)
    nom_semestre = models.CharField(max_length=255)
    order = models.IntegerField(blank=True)  # Consider adding validation for order

    def __str__(self):
        return f"{self.nom_semestre} - {self.niveau}"

    class Meta:
        unique_together = ('niveau', 'order') # Added unique together constraint

class Matier(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=10, default='DEFAULT_CODE', unique=True) # Added Uniq
    semester = models.ForeignKey(Semestre, on_delete=models.CASCADE, blank=True, null=True)
    specialite = models.ForeignKey(Specialite, on_delete=models.SET_NULL, null=True, blank=True) # Changed to SET_NULL
    is_common = models.BooleanField(default=False, help_text="True if this course is common to all specialties within the Niveau.")

    def __str__(self):
        if self.specialite and not self.is_common:
            return f"{self.code} - {self.name} - {self.specialite}"
        return f"{self.code} - {self.name} (Common)"  # Indicate common courses

    def clean(self):
        # Validation to ensure is_common and specialite are mutually exclusive
        if self.is_common and self.specialite:
            raise ValidationError("A course cannot be both common and have a specialty.")
        if not self.is_common and not self.specialite:
            raise ValidationError("A course must either be common or have a specialty.")
    def save(self, *args, **kwargs):
        self.full_clean()  # Ensure clean() is called
        super().save(*args, **kwargs)


class Etudiant(models.Model):
    Matricul = models.IntegerField(primary_key=True)
    nom_etudiant = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    sexe = models.CharField(max_length=255, blank=True, null=True)
    niveau = models.ForeignKey(Niveau, on_delete=models.CASCADE, blank=True, null=True)
    specialite = models.ForeignKey(Specialite, on_delete=models.SET_NULL, null=True, blank=True) # Changed to SET_NULL
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
      return f"{self.Matricul} - {self.nom_etudiant}"

    def clean(self):
        # Validation: L1 students cannot have a specialty, L2/L3 *must*
        if self.niveau:
            if self.niveau.nom_niveau == 'L1' and self.specialite:
                raise ValidationError({'specialite': "L1 students cannot have a specialty."})
            elif self.niveau.nom_niveau in ['L2', 'L3'] and not self.specialite:
                raise ValidationError({'specialite': "L2/L3 students must have a specialty."})
            # Ensure student's specialty matches Niveau's specialty (if applicable)
            if self.specialite and self.niveau and self.niveau.specialite and self.specialite != self.niveau.specialite:
                raise ValidationError({'specialite': "Student's specialty must match the Niveau's specialty."})

    def save(self, *args, **kwargs):
        self.full_clean()  # Ensure clean method is called
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if self.user:
            self.user.delete()  # Clean up associated User object
        super().delete(*args, **kwargs)

class Proffesseur(models.Model):
    id = models.IntegerField(primary_key=True)
    Nom_du_Prof = models.CharField(max_length=255)
    numero_tel = models.IntegerField()
    email = models.CharField(max_length=255)
    def __str__(self):
        return f"{self.Nom_du_Prof}" # Added string

class Section(models.Model):
    name = models.CharField(max_length=255)
    order = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.name}"

    class Meta:
        ordering = ['order']  # Consistent ordering
        unique_together = ('name', 'order') # Added unique together

class Question(models.Model):
    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name='questions')
    text = models.TextField(blank=True)
    choices = models.TextField(blank=True, null=True, help_text='Comma-separated list of choices')
    question_type = models.CharField(max_length=10, choices=[('radio', 'Radio'), ('input', 'Input')], default='radio')

    def get_choices(self):
        return [choice.strip() for choice in self.choices.split(',')] if self.choices else [] # Added condition

    def __str__(self):
        return f"{self.text}"

    def get_weight_for_choice(self, choice):
        choice_weights = {
            'Plutôt non': 1,
            'Non': 0,
            'Plutôt oui': 2,
            'Oui': 3,
        }
        return choice_weights.get(choice, 0)

class Questionnaire(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    professor = models.ForeignKey(Proffesseur, on_delete=models.CASCADE)
    matier = models.ForeignKey(Matier, on_delete=models.CASCADE)
    semester = models.ForeignKey(Semestre, on_delete=models.CASCADE)
    sections = models.ManyToManyField(Section, related_name='questionnaires', blank=True)
    expiration_time = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.sections.exists():
            sections = Section.objects.all()
            self.sections.set(sections)  # Consider restricting this in a real scenario

from django.db import models

class Datainserted(models.Model):
    questionnaire = models.ForeignKey('Questionnaire', on_delete=models.CASCADE)
    question = models.ForeignKey('Question', on_delete=models.CASCADE)
    section = models.ForeignKey('Section', on_delete=models.CASCADE)
    matier_code = models.CharField(max_length=10)
    weight = models.IntegerField()
    selected_choice = models.TextField()
    etudiant = models.ForeignKey('Etudiant', on_delete=models.SET_NULL, null=True)
    anne = models.ForeignKey('AnneeScolaire', on_delete=models.CASCADE, null=True)
    specialite = models.ForeignKey('Specialite', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.questionnaire} - {self.matier_code} - {self.question.text} - {self.section.name} - {self.specialite}"

    @staticmethod
    def calculate_percentage_for_section(questionnaire, section):
        data_inserted_objects = Datainserted.objects.filter(questionnaire=questionnaire, section=section)
        plustoNon_weight_sum = sum(obj.weight for obj in data_inserted_objects if obj.selected_choice == 'Plutôt non')
        POui_weight_sum = sum(obj.weight for obj in data_inserted_objects if obj.selected_choice == 'Plutôt oui')
        Oui_weight_sum = sum(obj.weight for obj in data_inserted_objects if obj.selected_choice == 'Oui')
        Non_weight_sum = sum(obj.weight for obj in data_inserted_objects if obj.selected_choice == 'Non')
        total_weighted_sum = Non_weight_sum + plustoNon_weight_sum + POui_weight_sum + Oui_weight_sum
        if total_weighted_sum == 0:
            return 0
        return (plustoNon_weight_sum / 3 + POui_weight_sum * 2 / 3 + Oui_weight_sum) / total_weighted_sum

    class Meta:
        unique_together = ('questionnaire', 'question', 'etudiant', 'anne', 'specialite')
        indexes = [
            models.Index(fields=['anne', 'specialite']),
            models.Index(fields=['questionnaire', 'etudiant']),
            models.Index(fields=['matier_code']),
        ]


# A simple caching mixin (optional) for frequently accessed querysets:
from django.core.cache import cache
from django.conf import settings
CACHE_TTL = getattr(settings, 'CACHE_TTL', 60 * 15)  # default 15 minutes

class CachedQueryMixin:
    @classmethod
    def get_cached_data(cls, key, queryset_func):
        data = cache.get(key)
        if data is None:
            data = list(queryset_func())
            cache.set(key, data, CACHE_TTL)
        return data

class Emailtable(models.Model):  # Not directly related to the core problem, but kept
    email = models.CharField(max_length=255)
    niveau = models.ForeignKey(Niveau, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.email} "

class Studentinfo(models.Model): # Consider if this is still needed
    id = models.AutoField(primary_key=True)
    student = models.ForeignKey(Etudiant, on_delete=models.CASCADE)
    matier = models.CharField(max_length=250)  # Might be redundant, consider removing
    url = models.URLField(blank=True)          # Might be redundant
    completed = models.BooleanField(default=False) # Might be redundant
    specialite = models.ForeignKey(Specialite, on_delete=models.SET_NULL, null=True, blank=True) # Added

    def __str__(self):
        return str(self.student.Matricul)
    

import asyncio
from django.db import transaction
from asgiref.sync import sync_to_async

class DataInsertionManager:
    BATCH_SIZE = 1000  # Adjust as needed

    @staticmethod
    async def bulk_insert_data(data_list, model_class):
        # Split the data_list into batches
        batches = [data_list[i:i + DataInsertionManager.BATCH_SIZE] 
                   for i in range(0, len(data_list), DataInsertionManager.BATCH_SIZE)]
        
        @sync_to_async
        def process_batch(batch):
            with transaction.atomic():
                model_class.objects.bulk_create(batch, batch_size=DataInsertionManager.BATCH_SIZE)

        # Process all batches concurrently
        await asyncio.gather(*[process_batch(batch) for batch in batches])

    @staticmethod
    async def process_questionnaire_responses(responses_data, model_class):
        # Create instances for each response
        data_instances = []
        for response in responses_data:
            data_instances.append(model_class(
                questionnaire_id=response['questionnaire_id'],
                question_id=response['question_id'],
                section_id=response['section_id'],
                matier_code=response['matier_code'],
                weight=response['weight'],
                selected_choice=response['selected_choice'],
                etudiant_id=response['etudiant_id'],
                anne_id=response['anne_id'],
                specialite_id=response['specialite_id']
            ))
            if len(data_instances) >= DataInsertionManager.BATCH_SIZE:
                await DataInsertionManager.bulk_insert_data(data_instances, model_class)
                data_instances = []
        if data_instances:
            await DataInsertionManager.bulk_insert_data(data_instances, model_class)
