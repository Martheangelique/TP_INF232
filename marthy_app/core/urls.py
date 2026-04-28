from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Interface d'administration Django
    path('admin/', admin.site.urls),
    
    # Inclusion des URLs de l'application surveillance
    path('surveillance/', include('surveillance.urls')),
    
    # Redirection optionnelle de la racine vers le dashboard
    path('', include('surveillance.urls')),
]