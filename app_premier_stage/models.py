from django.db import models
import uuid
from django.conf import settings

class Stagiaire(models.Model):
    id_stagiaire = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    nom_stagiaire = models.CharField(max_length=30,default="")
    prenom_stagiaire = models.CharField(max_length=100,default="")
    date_naissance_stagiaire = models.DateField()
    email_stagiaire = models.EmailField()
    telephone_stagiaire = models.CharField(max_length=15,default="+225")
    filiere_stagiaire = models.CharField(max_length=30,default="")
    cv_stagiaire = models.FileField()
    photo = models.ImageField()
    
    def __str__(self):
        return f"{self.nom_stagiaire} {self.prenom_stagiaire}"
class Entreprise(models.Model):
    id_entreprise = models.UUIDField(primary_key=True, default=uuid.uuid4,editable=False)
    nom_entreprise = models.CharField(max_length=30,default="")
    domaine_expertise = models.CharField(max_length=100,default="")
    localisation_entreprise = models.CharField(max_length=30,default="")

    def __str__(self):
        return f"{self.nom_entreprise}"

class OffreEmploi(models.Model):
    id_offre = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    titre_poste = models.CharField(max_length=30,default="")
    domaine_poste = models.CharField(max_length=100)
    description_offre = models.CharField(max_length=300,)
    type_offre = models.CharField(max_length=50)
    type_contrat = models.CharField()
    localisation_offre = models.CharField(max_length=100,default="")
    date_fin_candidature = models.DateField()
    entreprise = models.ForeignKey(Entreprise,on_delete=models.CASCADE)


    def __str__(self):
        return f"{self.titre_poste}"

class Candidature(models.Model):
    id_candidature = models.URLField(primary_key=True, default=uuid.uuid4,editable=False)
    stagiaire = models.ForeignKey(Stagiaire,on_delete=models.CASCADE, related_name='candidat')
    offre = models.ForeignKey(OffreEmploi,on_delete=models.CASCADE)
    satut_candidature = models.CharField(max_length=15,default="envoyee")
    date_postulation = models.DateTimeField(auto_created=True)

    def __str__(self):
        return    


