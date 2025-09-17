from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login,logout
from .models import Stagiaire,Entreprise,Candidature,OffreEmploi
from django.contrib.auth.models import Group, Permission
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator

def Index(request):
    return render(request,"home.html")

def Connexion(request):
    return render(request,"login.html")

def Deconnexion(request):
    logout(request)
    return redirect("connexion")

def DetailOffre(request):
    return render(request,"offre_detail.html")

@login_required(login_url="connexion")
def AdminDashboard(request):
    return render(request,"admin\dashboard.html")

def EntrepriseDashboard(request):
    return render(request,"entreprise\dashboard.html")

def DiplomeDashboard(request):
    return render(request,"diplome\dashboard.html")

def RegisterEntreprise(request):
    return render(request,"register_entreprise.html")

def RegisterDiplome(request):
    return render(request,"register_diplome.html")

@login_required(login_url="connexion")
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
        date_naissance_stagiaire=request.POST.get("date_naissance_stagiaire"),
        filiere_stagiaire=request.POST.get("filiere"),
        etablissement=request.POST.get("etablissement"),
        cv_stagiaire=request.FILES.get("cv"),
        photo=request.FILES.get("photo"),
    )
        messages.success("BIENVENUE SUR VOTRE PROFIL MON PREMIER STAGE")
        return redirect("diplome")
    return render(request,"completeprofil.html")
            

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
    return render(request,"diplome\offres.html",context=context)

@login_required(login_url="connexion")
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

        messages.success(request, "Vos informations ont bien été mises à jour ✅")
        return redirect("profilcandidat")

    return render(request, "diplome/profil.html", {"stagiaire": stagiaire})



def OffreDetail(request,pk):
    offre = get_object_or_404(OffreEmploi,id_offre=pk)
    context = {
        "offre":offre
    }
    return render(request,"diplome/offre_detail.html",context=context)

def OffreCree(request):
    return render(request,"entreprise\offre_create.html")