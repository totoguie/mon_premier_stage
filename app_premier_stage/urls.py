from . import views
from django.urls import path

urlpatterns = [
    path('',views.Index,name="Accueil"),
    path('Connexion/',views.Connexion,name='connexion'),
    path('detail/',views.DetailOffre,name='detail'),
    path('entreprise/',views.EntrepriseDashboard,name='entreprise'),
    path('diplome/',views.DiplomeDashboard,name='diplome'),
    path('admindashboard/',views.AdminDashboard,name='admindashboard'),
]
