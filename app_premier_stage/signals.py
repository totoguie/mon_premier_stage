from django.db.models.signals import post_migrate,post_save
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.dispatch import receiver
from .models import Stagiaire, OffreEmploi, Candidature


@receiver(post_migrate)
def create_default_groups(sender, **kwargs):
    stagiaire_groupe, _ = Group.objects.get_or_create(name="stagiaire")
    entreprise_groupe, _ = Group.objects.get_or_create(name="entreprise")
    administrateur_group, _ = Group.objects.get_or_create(name="administrateur") 

    #Permission pour stagigiaire
    ct_stagiaire = ContentType.objects.get_for_model(Stagiaire)
    can_change_stagiaire = Permission.objects.get(codename="change_stagiaire")
    can_add_stagiaire = Permission.objects.get(codename="add_stagiaire")
    can_view_stagiaire = Permission.objects.get(codename="view_stagiaire")
    can_delete_stagiaire = Permission.objects.get(codename="delete_stagiaire")

    #Permission pour offre d'emploi
    ct_offre = ContentType.objects.get_for_model(OffreEmploi)
    can_view_offres = Permission.objects.get(codename="view_offreemploi", content_type=ct_offre)
    can_add_offres = Permission.objects.get(codename="add_offreemploi", content_type=ct_offre)
    can_change_offres = Permission.objects.get(codename="change_offreemploi", content_type=ct_offre)
    can_delete_offres = Permission.objects.get(codename="delete_offreemploi", content_type=ct_offre)

    # Permissions pour le modèle Candidature
    ct_candidature = ContentType.objects.get_for_model(Candidature)
    can_add_candidature = Permission.objects.get(codename="add_candidature", content_type=ct_candidature)
    can_delete_candidature = Permission.objects.get(codename="delete_candidature", content_type=ct_candidature)
    can_view_candidature = Permission.objects.get(codename="view_candidature", content_type=ct_candidature)
    
    # Attribution des permissions
    stagiaire_groupe.permissions.add(
        can_view_offres, 
        can_add_candidature,
        can_view_candidature,
        can_change_stagiaire,
        can_add_stagiaire
        )
    
    entreprise_groupe.permissions.add(
        can_add_offres,
        can_change_offres,
        can_delete_offres,
        can_view_candidature,
        can_view_stagiaire
        )
    
    administrateur_group.permissions.add(
        can_view_offres, 
        can_add_candidature,
        can_view_candidature,
        can_change_stagiaire,
        can_add_stagiaire,
        can_delete_stagiaire,
        can_add_offres,
        can_change_offres,
        can_delete_offres,
        can_view_candidature,
        can_view_stagiaire,
        can_add_offres,
        can_change_offres,
        can_delete_offres,
        can_view_candidature,
        can_view_stagiaire,
    )

    print("Groupes et permissions par défaut créés avec succès !")

@receiver(post_save, sender=Stagiaire)
def add_user_to_stagiaire_group(sender, instance, created, **kwargs):
    """
    Quand un Stagiaire est créé :
    - Ajoute l'utilisateur au groupe 'stagiaire'
    - Définit son rôle
    - Marque son profil comme complété
    - Active le compte
    """
    if created:
        stagiaire_groupe, _ = Group.objects.get_or_create(name="stagiaire")
        instance.user.groups.add(stagiaire_groupe)

        # On s'assure que les attributs existent sur le modèle User
        instance.user.role = "stagiaire"
        instance.user.is_profile_completed = True
        instance.user.is_active = True  # 🔑 activation du compte après completion
        instance.user.save()