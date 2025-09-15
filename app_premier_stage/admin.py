from django.contrib import admin
from .models import User, Candidature, Stagiaire, Entreprise, OffreEmploi

admin.site.register(User)
admin.site.register(Stagiaire)
admin.site.register(Entreprise)
admin.site.register(OffreEmploi)
admin.site.register(Candidature)
