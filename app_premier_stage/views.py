from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login,logout,authenticate
from .models import Stagiaire,Entreprise,Candidature,OffreEmploi,User
from django.contrib.auth.models import Group, Permission
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from django.contrib.auth.decorators import user_passes_test
from django.db import transaction


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
    return render(request,"admin\dashboard.html")

def Statistiques(request):
    return render(request,"admin/statisques.html")


def EntrepriseDashboard(request):
    # if not is_entreprise(user=request.user):
    #     messages.error(request,"Vous n'êtes pas autoriser")
    #     return redirect("connexion")
    return render(request,"entreprise\dashboard.html")

@login_required(login_url="connexion")
def DiplomeDashboard(request):
    if not is_stagiaire(user=request.user):
        messages.error(request,"Vous n'êtes pas autoriser")
        return redirect("connexion")
    return render(request,"diplome\dashboard.html")

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
            user = User.objects.create(
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


user_passes_test(is_administrateur,login_url="connexion")
def ValiderEntreprise(request,user_id):
    user = get_object_or_404(User,id=user_id)
    user.is_active = True
    user.save()
    messages.success(request,f"Le compte de {user.username} a été validé avec succès.")
    return redirect("")

def RegisterDiplome(request):
    return render(request,"diplome/register_diplome.html")

@login_required(login_url="connexion")
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
        messages.success("BIENVENUE SUR VOTRE PROFIL MON PREMIER STAGE")
        return redirect("diplome")
    return render(request,"diplome/completeprofil.html")

@login_required(login_url="connexion")
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

def DetailOffre(request):
    # offre = get_object_or_404(OffreEmploi,id_offre=pk)
    # context = {
    #     "offre":offre
    # }
    return render(request,"diplome/offre_detail.html")


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
    return render(request,"diplome\candidature_detail.html",context=context)

def OffreCree(request):
    return render(request,"entreprise\offre_create.html")

def Listecandidature(request):
    return render(request,"entreprise/candidature_offres.html")

def Detailcandidat(request):
    return render(request,"entreprise/detail_candidat.html")