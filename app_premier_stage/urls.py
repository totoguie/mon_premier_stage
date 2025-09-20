from . import views
from django.urls import path

urlpatterns = [
    path('',views.Index,name="Accueil"),
    path('Connexion/',views.Connexion,name='connexion'),
    path('Deconnexion',views.Deconnexion,name="deconnexion"),
    path('detailoffre/',views.DetailOffre,name='detail'),
    path('entreprise/',views.EntrepriseDashboard,name='entreprise'),
    path('diplome/',views.DiplomeDashboard,name='diplome'),
    path('admindashboard/',views.AdminDashboard,name='admindashboard'),
    path('statistique/',views.Statistiques,name="statistique"),
    path('preinscription/',views.Preinscription,name="preinscription"),
    path('inscriptionDiplome/',views.RegisterDiplome,name="inscriptionDiplome"),
    path('completeprofil/',views.CompleteProfil,name="completeprofil"),
    path('inscriptionEntreprise/',views.RegisterEntreprise,name="inscriptionEntreprise"),
    path('detailCandidature/<pk>/',views.DetailCandidature,name="detailCandidature"),
    path('candidature/',views.Mescandidatures,name='candidature'),
    path('offres/',views.Offres,name='offres'),
    path('profilCandidat/',views.profilUpdate,name='profilcandidat'),
    path('offreCree/',views.OffreCree,name='offrecree'),
    path('listecandidature/',views.Listecandidature,name="liste_candidatures"),
    path('detailcandidat/',views.Detailcandidat,name="detailcandidat"),
    path("listeentreprise/",views.ListeEntreprise,name="liste_entreprise"),
    path("listeoffre/",views.ListeOffre,name="liste_offres"),
    path("listestagiaire/",views.ListeStagiaire,name="liste_stagiaires"),

]

