from django.shortcuts import render

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

def RegisterDiplome(request):
    if request.method == "post":
        nom = request.post.get("nom")
        email = request.post.get("email")
        password = request.post.get("password")
        
    return render(request,"register_diplome.html")

def RegisterEntreprise(request):
    return render(request,"register_entreprise.html")

def DetailCandidature(request):
    return render(request,"diplome\candidature_detail.html")

def Candidature(request):
    return render(request,"diplome\candidatures.html")

def Offres(request):
    return render(request,"diplome\offres.html")

def profilCandidat(request):
    return render(request,"diplome\profil.html")

def OffreDetail(request):
    return render(request,"diplome\offre_detail.html")

def OffreCree(request):
    return render(request,"entreprise\offre_create.html")