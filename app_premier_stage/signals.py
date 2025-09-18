from django.db.models.signals import post_migrate, post_save
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.dispatch import receiver
from .models import Stagiaire, OffreEmploi, Candidature, Entreprise


@receiver(post_migrate)
def create_default_groups(sender, **kwargs):
    stagiaire_groupe, _ = Group.objects.get_or_create(name="stagiaire")
    entreprise_groupe, _ = Group.objects.get_or_create(name="entreprise")
    administrateur_group, _ = Group.objects.get_or_create(name="administrateur") 

    # Permissions Stagiaire
    ct_stagiaire = ContentType.objects.get_for_model(Stagiaire)
    can_change_stagiaire, _ = Permission.objects.get_or_create(
        codename="change_stagiaire",
        content_type=ct_stagiaire,
        defaults={"name": "Can change stagiaire"}
    )
    can_add_stagiaire, _ = Permission.objects.get_or_create(
        codename="add_stagiaire",
        content_type=ct_stagiaire,
        defaults={"name": "Can add stagiaire"}
    )
    can_view_stagiaire, _ = Permission.objects.get_or_create(
        codename="view_stagiaire",
        content_type=ct_stagiaire,
        defaults={"name": "Can view stagiaire"}
    )
    can_delete_stagiaire, _ = Permission.objects.get_or_create(
        codename="delete_stagiaire",
        content_type=ct_stagiaire,
        defaults={"name": "Can delete stagiaire"}
    )

    # Permissions Offre d'emploi
    ct_offre = ContentType.objects.get_for_model(OffreEmploi)
    can_view_offres, _ = Permission.objects.get_or_create(
        codename="view_offreemploi",
        content_type=ct_offre,
        defaults={"name": "Can view offre emploi"}
    )
    can_add_offres, _ = Permission.objects.get_or_create(
        codename="add_offreemploi",
        content_type=ct_offre,
        defaults={"name": "Can add offre emploi"}
    )
    can_change_offres, _ = Permission.objects.get_or_create(
        codename="change_offreemploi",
        content_type=ct_offre,
        defaults={"name": "Can change offre emploi"}
    )
    can_delete_offres, _ = Permission.objects.get_or_create(
        codename="delete_offreemploi",
        content_type=ct_offre,
        defaults={"name": "Can delete offre emploi"}
    )

    # Permissions Candidature
    ct_candidature = ContentType.objects.get_for_model(Candidature)
    can_add_candidature, _ = Permission.objects.get_or_create(
        codename="add_candidature",
        content_type=ct_candidature,
        defaults={"name": "Can add candidature"}
    )
    can_delete_candidature, _ = Permission.objects.get_or_create(
        codename="delete_candidature",
        content_type=ct_candidature,
        defaults={"name": "Can delete candidature"}
    )
    can_view_candidature, _ = Permission.objects.get_or_create(
        codename="view_candidature",
        content_type=ct_candidature,
        defaults={"name": "Can view candidature"}
    )

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
        can_view_stagiaire,
    )

    print("✅ Groupes et permissions par défaut créés avec succès !")


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

@receiver(post_save, sender=Entreprise)
def add_user_entreprise_to_entreprise_group(sender, instance, created, *args, **kwargs):
    if created:
        entreprise_groupe, _= Group.objects.get_or_create(name="entreprise")

        instance.user.role = "entreprise"
        instance.user.save()