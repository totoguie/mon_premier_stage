from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login,logout,authenticate
from .models import Stagiaire,Entreprise,Candidature,OffreEmploi,User
from django.contrib.auth.models import Group, Permission
from django.contrib import messages
from django.db.models import Q,Count
from django.utils import timezone
from django.core.paginator import Paginator
from django.contrib.auth.decorators import user_passes_test
from django.db import transaction
import json


def Index(request):
    return render(request,"home.html")

def is_entreprise(user):
    return user.groups.filter(name="entreprise").exists()

def is_administrateur(user):
    return user.groups.filter(name="administrateur").exists()

def is_stagiaire(user):
    return user.groups.filter(name="stagiaire").exists()

@transaction.atomic
def Connexion(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user= User.objects.get(username=username)
        print(user.username)
        print(user.password)

        if username and password:
            user = authenticate(request, username=username, password=password)
            if user is not None: 
                if is_entreprise(user):
                    login(request, user)
                    return redirect("entreprise")

                elif is_administrateur(user):
                    login(request, user)
                    return redirect("admindashboard")

                elif is_stagiaire(user):
                    login(request, user)
                    return redirect("diplome")

                else:
                    messages.error(request, "Votre rôle n'est pas reconnu.")
                    return redirect("connexion")
            else:
                messages.error(request, "Nom d'utilisateur ou mot de passe incorrect.")
                return redirect("connexion")
        else:
            messages.error(request, "Veuillez bien renseigner le formulaire.")
            return redirect("connexion")

    return render(request, "login.html")


def Deconnexion(request):
    logout(request)
    messages.success(request,"Déconnexion réussie")
    return redirect("connexion")

#@login_required(login_url="connexion")
def AdminDashboard(request):
    # if not is_administrateur(user=request.user):
    #     messages.error(request,"Vous n'êtes pas autoriser")
    #     return redirect("connexion")
    total_stagiaire = Stagiaire.objects.count()
    total_entreprise = Entreprise.objects.count()
    total_offre = OffreEmploi.objects.count()

    dernier_utilisateur = User.objects.order_by("-id")[:3]

    offre_recente = OffreEmploi.objects.order_by("-id_offre")[:5]
    entreprise_en_attente = Entreprise.objects.filter(validation_entreprise=False).order_by("-id_entreprise")[:5]
    context = {
        "total_stagiaire":total_stagiaire,
        "total_entreprise":total_entreprise,
        "total_offre":total_offre,
        "dernier_utilisateur":dernier_utilisateur,
        "offre_recente":offre_recente,
        "entreprise_en_attente":entreprise_en_attente
    }
    
    return render(request,"admin/dashboard.html",context=context)

def Statistiques(request):
    year = request.GET.get("year", timezone.now().year)

    offres_par_mois = (
        OffreEmploi.objects.filter(created_at__year=year)
        .extra(select={"month": "strftime('%%m', created_at)"})
        .values("month")
        .annotate(total=Count("id_offre"))
        .order_by("month")
    )

    entreprises_par_mois = (
        Entreprise.objects.filter(created_at__year=year)
        .extra(select={"month": "strftime('%%m', created_at)"})
        .values("month")
        .annotate(total=Count("id_entreprise"))
        .order_by("month")
    )

    candidatures_par_mois = (
        Candidature.objects.filter(created_at__year=year)
        .extra(select={"month": "strftime('%%m', created_at)"})
        .values("month")
        .annotate(total=Count("id_candidature"))
        .order_by("month")
    )

    stagiaires_par_mois = (
        Stagiaire.objects.filter(created_at__year=year)
        .extra(select={"month": "strftime('%%m', created_at)"})
        .values("month")
        .annotate(total=Count("id_stagiaire"))
        .order_by("month")
    )

    context = {
        "year": int(year),
        "offres_par_mois": json.dumps(list(offres_par_mois)),
        "entreprises_par_mois": json.dumps(list(entreprises_par_mois)),
        "candidatures_par_mois": json.dumps(list(candidatures_par_mois)),
        "stagiaires_par_mois": json.dumps(list(stagiaires_par_mois)),
    }
    return render(request, "admin/statistiques.html", context)


def EntrepriseDashboard(request):
    if not is_entreprise(user=request.user):
        messages.error(request, "Vous n'êtes pas autorisé")
        return redirect("connexion")

    entreprise = Entreprise.objects.get(user=request.user)

    # --- Statistiques
    offres_actives = OffreEmploi.objects.filter(entreprise=entreprise,statut_offre="disponible").count()
    candidatures_total = Candidature.objects.filter(offre__entreprise=entreprise).count()
    candidats_preselectionnes = Candidature.objects.filter(offre__entreprise=entreprise, statut_candidature="preselectionne").count()
    entretiens_planifies = Candidature.objects.filter(offre__entreprise=entreprise, statut_candidature="entretien").count()

    # --- Offres de l’entreprise
    offres = OffreEmploi.objects.filter(entreprise=entreprise).order_by("-created_at")

    # --- Recherche de stagiaires
    filiere_filter = request.GET.get("filiere", "")
    query = request.GET.get("q", "")

    stagiaires = Stagiaire.objects.all()
    if filiere_filter:
        stagiaires = stagiaires.filter(filiere_stagiaire=filiere_filter)
    if query:
        stagiaires = stagiaires.filter(
            Q(nom_stagiaire__icontains=query) |
            Q(prenom_stagiaire__icontains=query) |
            Q(etablissement__icontains=query)
        )

    # --- Liste unique des filières
    filieres = Stagiaire.objects.values_list("filiere_stagiaire", flat=True).distinct()

    context = {
        "offres_actives": offres_actives,
        "candidatures_total": candidatures_total,
        "candidats_preselectionnes": candidats_preselectionnes,
        "entretiens_planifies": entretiens_planifies,
        "offres": offres,
        "stagiaires": stagiaires[:12],  # on limite pour ne pas surcharger la page
        "filieres": filieres,
    }
    return render(request, "entreprise/dashboard.html", context)

@login_required(login_url="connexion")
def DiplomeDashboard(request):
    if not is_stagiaire(user=request.user):
        messages.error(request,"Vous n'êtes pas autoriser")
        return redirect("connexion")
    return render(request,"diplome/dashboard.html")

def Preinscription(request):
    return render(request,"preinscription.html")

@transaction.atomic
def RegisterEntreprise(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email_entreprise = request.POST.get("email")
        password = request.POST.get("password")
        nom_entreprise = request.POST.get("nom_entreprise")
        secteur = request.POST.get("secteur")
        localisation = request.POST.get("localisation")
        telephone_entreprise = request.POST.get("telephone_entreprise")
        nombre_employe = request.POST.get("nombre_employe")

        if User.objects.filter(username=username).exists():
            messages.error(request,"Nom d'utilisateur déjà existant,veuillez en choisir un autre.")
            return redirect("inscriptionEntreprise")
        else:
            user = User.objects.create_user(
                username = username,
                password = password,
                email = email_entreprise,
                is_active = False
            )

            Entreprise.objects.create(
                user = user,
                nom_entreprise = nom_entreprise,
                domaine_expertise = secteur,
                telephone_entreprise = telephone_entreprise,
                email_entreprise = email_entreprise,
                nombre_employe = nombre_employe,
                localisation_entreprise = localisation
            )

            messages.info(request,"Votre inscription a été transmis aux administrateur pour validation.")
            return redirect("inscriptionEntreprise")
    return render(request,"entreprise/registerEntreprise.html")


#user_passes_test(is_administrateur,login_url="connexion")
def ValiderEntreprise(request,pk):
    entreprise = get_object_or_404(Entreprise,id_entreprise=pk)
    user = entreprise.user
    entreprise.validation_entreprise = True
    user.is_active = True
    user.is_profile_completed = True
    user.save()
    entreprise.save()
    messages.success(request,f"Le compte a été validé avec succès.")
    return redirect("admindashboard")

def RegisterDiplome(request):
    return render(request,"diplome/register_diplome.html")

user_passes_test(is_stagiaire,login_url="connexion")
@transaction.atomic
def CompleteProfil(request):
    messages.info(request,
                  "Veuillez remplir ce formulaire pour compléter vos information et activer votre compte"
                  )
    user = request.user

    if hasattr(user, "profil_stagiaire"):
        return redirect("diplome")  

    if request.method == "POST":
        Stagiaire.objects.create(
        user=user,
        nom_stagiaire=request.POST.get("nom"),
        prenom_stagiaire=request.POST.get("prenom"),
        telephone_stagiaire=request.POST.get("telephone"),
        email_stagiaire = user.email,
        date_naissance_stagiaire=request.POST.get("date_naissance_stagiaire"),
        filiere_stagiaire=request.POST.get("filiere"),
        etablissement=request.POST.get("etablissement"),
        cv_stagiaire=request.FILES.get("cv"),
        photo=request.FILES.get("photo"),
    )
        messages.success(request,"BIENVENUE SUR VOTRE PROFIL MON PREMIER STAGE")
        return redirect("diplome")
    return render(request,"diplome/completeprofil.html")

user_passes_test(is_stagiaire,login_url="connexion")
@transaction.atomic
def profilUpdate(request):
    stagiaire = get_object_or_404(Stagiaire, user=request.user)

    if request.method == "POST":
        stagiaire.nom_stagiaire = request.POST.get("nom_stagiaire") or stagiaire.nom_stagiaire
        stagiaire.prenom_stagiaire = request.POST.get("prenom_stagiaire") or stagiaire.prenom_stagiaire
        stagiaire.etablissement = request.POST.get("etablissement") or stagiaire.etablissement
        stagiaire.telephone_stagiaire = request.POST.get("telephone_stagiaire") or stagiaire.telephone_stagiaire
        stagiaire.email_stagiaire = request.POST.get("email_stagiaire") or stagiaire.email_stagiaire
        stagiaire.filiere_stagiaire = request.POST.get("filiere_stagiaire") or stagiaire.filiere_stagiaire

        if request.FILES.get("cv_stagiaire"):
            stagiaire.cv_stagiaire = request.FILES["cv_stagiaire"]

        stagiaire.save()

        messages.success(request, "Vos informations ont bien été mises à jour")
        return redirect("profilcandidat")

    return render(request, "diplome/profil.html", {"stagiaire": stagiaire})

def Offres(request):
    try:
        stagiaire = get_object_or_404(Stagiaire,user=request.user)
    except Stagiaire.DoesNotExist:
        messages.error(request,"Utilisateur inexistant")
        return redirect ("inscriptionDiplome")
    
        
    offre = OffreEmploi.objects.filter(domaine_poste__icontains=stagiaire.filiere_stagiaire).select_related("entreprise")
    query = request.GET.get("recherche")
    if query:
        offre = offre.filter(
            Q(titre_poste__icontains = query),
            Q(localisation_offre__icontains =query),
            Q(domaine_poste__icontains=query)
        )
    paginator = Paginator(offre,5)
    pages = request.GET.get("page")
    offres = paginator.get_page(pages)
    context = {
        "offres":offres,
        "stagiaire":stagiaire
    }
    return render(request,"diplome/offres.html",context=context)

def DetailOffre(request,pk):
    offre = get_object_or_404(OffreEmploi,id_offre=pk)
    context = {
        "offre":offre
    }
    return render(request,"diplome/offre_detail.html",context)


def Mescandidatures(request):
    candidatures = (
        Candidature.objects
        .filter(stagiaire__user=request.user)
        .select_related("offre", "stagiaire", "offre__entreprise")
        .order_by("-date_postulation")  # pour voir la plus récente en premier
    )
    return render(request, "diplome/candidatures.html", {"candidatures": candidatures})

def DetailCandidature(request,pk):
    candidature = Candidature.objects.get(id_candidature=pk)
    context = {
        "candidature":candidature
    }
    return render(request,"diplome/candidature_detail.html",context=context)

@user_passes_test(is_entreprise, login_url="connexion")
@transaction.atomic
def OffreCree(request):
    if request.method == "POST":
        try:
            # Récupération entreprise liée au user connecté
            entreprise = get_object_or_404(Entreprise, user=request.user)

            # Création de l'offre
            offre = OffreEmploi.objects.create(
                user=request.user,
                entreprise=entreprise,
                titre_poste=request.POST.get("titre_poste"),
                domaine_poste=request.POST.get("domaine_poste"),
                type_offre=request.POST.get("type_offre"),
                type_contrat=request.POST.get("type_contrat"),
                duree_contrat=request.POST.get("duree_contrat"),
                date_debut_offre=request.POST.get("date_debut_offre"),
                date_fin_candidature=request.POST.get("date_fin_candidature"),
                remuneration_offre=request.POST.get("remuneration_offre"),
                localisation_offre=request.POST.get("localisation_offre"),
                description_offre=request.POST.get("description_offre"),
                competence_requis=request.POST.get("competence_requis"),
                mission_offre=request.POST.get("mission_offre")
            )

            messages.success(request, "✅ Offre ajoutée avec succès")
            return redirect("entreprise")

        except Exception as e:
            messages.error(request, f"❌ Erreur : {e}")
            return redirect("offrecree")

    return render(request, "entreprise/offre_create.html")

def Listecandidature(request):
    return render(request,"entreprise/candidature_offres.html")

def Detailcandidat(request,pk):
    return render(request,"entreprise/detail_candidat.html")

def ListeEntreprise(request):
    entreprise = Entreprise.objects.all()
    context = {
        "entreprise":entreprise
    }
    return render(request,"admin/liste_entreprises.html",context=context)

def ListeOffre(request):
    offres = OffreEmploi.objects.all()
    context = {
        "offres":offres
    }
    return render(request,"admin/liste_offres.html",context)

def ListeStagiaire(request):
    stagiaires = Stagiaire.objects.all()
    context = {
        "stagiaires":stagiaires
    }
    return render(request,"admin/liste_stagiaires.html",context=context)

def AdminCandidature(request):
    candidatures = Candidature.objects.all()
    context = {
        "candidatures":candidatures
    }
    return render(request,"admin/liste_candidatures.html",context)

def AdminDetailCandidature(request,pk):
    candidature = get_object_or_404(Candidature,candidature_id=pk)
    context = {
        "candidature":candidature
    }
    return render(request,"admin/detail_candidature.html",context)

def AdminDetailStagiaire(request,pk):
    stagiaire = get_object_or_404(Stagiaire,id_stagiaire=pk)
    context = {
        "stagiaire":stagiaire
    }
    return render(request,"admin/detail_stagiaire.html",context)

def AdminDetailEntreprise(request,pk):
    entreprise = get_object_or_404(Entreprise,id_entreprise=pk)
    context = {
        "entreprise":entreprise
    }
    return render(request,"admin/detail_entreprise.html",context=context)