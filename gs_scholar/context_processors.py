from .models import AnneeScolaire

def current_annee_scolaire(request):
    current_annee = AnneeScolaire.objects.filter(current=True).first()
    previous = current_annee.annee - 1
    return {'current_annee': current_annee,'previous':previous}
