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