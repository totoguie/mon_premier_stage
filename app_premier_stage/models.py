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
    telephone_entreprrise = models.CharField(max_length=15,default="")
    email_entreprise = models.EmailField(default="")
    nombre_employe = models.CharField(max_length=20,default="")
    localisation_entreprise = models.CharField(max_length=30, default="")

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
    domaine_poste = models.CharField(max_length=100)
    description_offre = models.TextField(max_length=1000)
    type_offre = models.CharField(max_length=50)
    type_contrat = models.CharField(max_length=50)
    competence_requis = models.CharField(max_length=250,default="")
    duree_contrat = models.DateField()
    date_debut_offre = models.DateField()
    remuneration_offre = models.CharField(max_length=10,default="")
    mission_offre = models.CharField(max_length=300,default="")
    localisation_offre = models.CharField(max_length=100, default="")
    date_fin_candidature = models.DateField()

    def __str__(self):
        return f"{self.titre_poste} - {self.entreprise.nom_entreprise}"


class Candidature(models.Model):
    id_candidature = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    stagiaire = models.ForeignKey(Stagiaire, on_delete=models.CASCADE, related_name="candidat")
    offre = models.ForeignKey(OffreEmploi, on_delete=models.CASCADE, related_name="offre_postule")
    statut_candidature = models.CharField(max_length=15, default="envoyée")
    date_postulation = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["stagiaire", "offre"], name="unique_candidature")
        ]

    def __str__(self):
        return f"Candidature de {self.stagiaire.nom_stagiaire} à {self.offre.titre_poste}"
