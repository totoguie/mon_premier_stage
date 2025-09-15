from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from .models import Stagiaire,Entreprise,Candidature
from django.views import View
from django.db.models.signals import post_migrate, post_save
from django.dispatch import receiver
from django.contrib.auth.models import Group, Permission

def Index(request):
    return render(request,"home.html")

def Connexion(request):
    return render(request,"login.html")

def DetailOffre(request):
    return render(request,"offre_detail.html")

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
    user = request.user

    # 🔒 Vérifie si le profil existe déjà
    if hasattr(user, "profil_stagiaire"):
        return redirect("diplome")  # déjà créé → on bloque

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
        return redirect("diplome")
    return render(request,"completeprofil.html")


            
def DetailCandidature(request):
    return render(request,"diplome\candidature_detail.html")

def Postuler(request):
    return render(request,"diplome\candidatures.html")

def Offres(request):
    return render(request,"diplome\offres.html")

def profilCandidat(request):
    return render(request,"diplome\profil.html")

def OffreDetail(request):
    return render(request,"diplome\offre_detail.html")

def OffreCree(request):
    return render(request,"entreprise\offre_create.html")