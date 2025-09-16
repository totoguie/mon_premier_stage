from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from .models import Stagiaire,Entreprise,Candidature
from django.views import View
from django.db.models.signals import post_migrate, post_save
from django.dispatch import receiver
from django.contrib.auth.models import Group, Permission
from django.contrib import messages

def Index(request):
    return render(request,"home.html")

def Connexion(request):
    return render(request,"login.html")

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
    return render(request,"diplome\offres.html")

def profilCandidat(request):
    stagiaire = Stagiaire.objects.get(user=request.user)
    return render(request,"diplome\profil.html")

def OffreDetail(request):
    return render(request,"diplome\offre_detail.html")

def OffreCree(request):
    return render(request,"entreprise\offre_create.html")