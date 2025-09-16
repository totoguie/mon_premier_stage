from . import views
from django.urls import path

urlpatterns = [
    path('',views.Index,name="Accueil"),
    path('Connexion/',views.Connexion,name='connexion'),
    path('detail/',views.DetailOffre,name='detail'),
    path('entreprise/',views.EntrepriseDashboard,name='entreprise'),
    path('diplome/',views.DiplomeDashboard,name='diplome'),
    path('admindashboard/',views.AdminDashboard,name='admindashboard'),
    path('inscriptionDiplome/',views.RegisterDiplome,name="inscriptionDiplome"),
    path('completeprofil/',views.CompleteProfil,name="completeprofil"),
    path('inscriptionEntreprise/',views.RegisterEntreprise,name="inscriptionEntreprise"),
    path('detailCandidature/<pk>/',views.DetailCandidature,name="detailCandidature"),
    path('candidature/',views.Mescandidatures,name='candidature'),
    path('offres/',views.Offres,name='offres'),
    path('profilCandidat/',views.profilCandidat,name='profilcandidat'),
    path('offreDetail/',views.OffreDetail,name='offredetail'),
    path('offreCree/',views.OffreCree,name='offrecree'),
]

