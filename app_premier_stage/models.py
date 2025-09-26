from django.db import models
import uuid
from django.conf import settings
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLES_CHOICES = (
        ("stagiaire", "Stagiaire"),
        ("entreprise", "Entreprise"),
        ("administrateur", "Administrateur"),
    )
    role = models.CharField(max_length=20, choices=ROLES_CHOICES, default="stagiaire")
    is_profile_completed = models.BooleanField(default=False)


class Stagiaire(models.Model):
    id_stagiaire = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profil_stagiaire"
    )
    nom_stagiaire = models.CharField(max_length=30, default="")
    prenom_stagiaire = models.CharField(max_length=100, default="")
    etablissement = models.CharField(max_length=50, default="")
    date_naissance_stagiaire = models.DateField()
    telephone_stagiaire = models.CharField(max_length=15, default="+225")
    email_stagiaire = models.EmailField(max_length=30,default="")
    filiere_stagiaire = models.CharField(max_length=30, default="")
    cv_stagiaire = models.FileField(upload_to="cvs/", blank=True, null=True)
    photo = models.ImageField(upload_to="photos/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.nom_stagiaire} {self.prenom_stagiaire}"

class Entreprise(models.Model):
    id_entreprise = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profil_entreprise"
    )
    nom_entreprise = models.CharField(max_length=30, default="")
    domaine_expertise = models.CharField(max_length=100, default="")
    telephone_entreprise = models.CharField(max_length=15,default="")
    email_entreprise = models.EmailField(default="")
    nombre_employe = models.CharField(max_length=20,default="",null=True, blank=True)
    site_entreprise = models.URLField(default="",null=True, blank=True)
    validation_entreprise = models.BooleanField(default=False)
    localisation_entreprise = models.CharField(max_length=30, default="")
    description_entreprise = models.CharField(max_length=100,default="",null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nom_entreprise}"

class OffreEmploi(models.Model):
    id_offre = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="offres_entreprise",
        default=""
    )
    entreprise = models.ForeignKey(Entreprise, on_delete=models.CASCADE, related_name="offres")
    titre_poste = models.CharField(max_length=30, default="")
    domaine_poste = models.CharField(max_length=100,default="")
    description_offre = models.TextField(max_length=1000,default="",null=True, blank=True)
    type_offre = models.CharField(max_length=150,default="")
    type_contrat = models.CharField(max_length=150,default="",null=True, blank=True)
    competence_requis = models.CharField(max_length=250,default="",null=True, blank=True)
    duree_contrat = models.CharField(max_length=20,default="",null=True, blank=True)
    date_debut_offre = models.DateField()
    remuneration_offre = models.CharField(max_length=10,default="",null=True, blank=True)
    mission_offre = models.CharField(max_length=300,default="",null=True, blank=True)
    localisation_offre = models.CharField(max_length=100, default="")
    statut_offre = models.CharField(max_length=20,default="disponible")
    date_fin_candidature = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.titre_poste} - {self.entreprise.nom_entreprise}"


class Candidature(models.Model):
    id_candidature = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    stagiaire = models.ForeignKey(Stagiaire, on_delete=models.CASCADE, related_name="candidat")
    offre = models.ForeignKey(OffreEmploi, on_delete=models.CASCADE, related_name="offre_postule")
    statut_candidature = models.CharField(max_length=15, default="candidature envoyée")
    date_postulation = models.DateTimeField(auto_now_add=True)
    date_entretien = models.DateField(null=True, blank=True)
    heure_entretien = models.TimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["stagiaire", "offre"], name="unique_candidature")
        ]

    def __str__(self):
        return f"Candidature de {self.stagiaire.nom_stagiaire} à {self.offre.titre_poste}"
