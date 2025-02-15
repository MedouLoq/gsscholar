from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import *

@receiver(post_save, sender=Questionnaire)
def connect_questionnaire_to_sections(sender, instance, created, **kwargs):

    if created:
        sections = Section.objects.all()
        instance.sections.set(sections)

# Signal to update related Niveaux when a new AnneeScolaire is saved
@receiver(post_save, sender=AnneeScolaire)
def update_related_niveaux(sender, instance, created, **kwargs):
    # if created and instance.current:
    #     instance.update_related_niveaux()
    pass

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Etudiant
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
@receiver(post_save, sender=Etudiant)
def create_user_and_send_email(sender, instance, created, **kwargs):
    if created:
        # Generate a random password (you may want a more secure method)
        password = User.objects.make_random_password()

        # Create a new user
        user = User.objects.create(username=instance.email, email=instance.email)
        user.set_password(password)
        user.save()

        # Link the user to the student
        instance.user = user
        instance.save()

        # Render HTML content from the template file
        html_content = render_to_string('mail.html', {
            'first_name': instance.nom_etudiant,
            'last_name': instance.Matricul,
            'platform_link': 'http://127.0.0.1:8000',  # Update with your actual link
            'username': user.username,
            'password': password,
        })

        # Send email with the generated password and custom message
        subject = 'Evaluation des enseignements'
        from_email = 'babeabdellahi5@gmail.com'  # Replace with your actual email
        to_email = [user.email]

        email = EmailMessage(subject, html_content, from_email, to_email)
        email.content_subtype = 'html'  # Enable HTML content in the email
        email.send()
