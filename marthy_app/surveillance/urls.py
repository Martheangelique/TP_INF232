# from django.urls import path
# from . import views

# urlpatterns = [
#     # Page d'accueil de l'application (le Dashboard)
#     path('', views.dashboard, name='dashboard'),
    
#     # Page du formulaire de saisie
#     path('nouveau/', views.nouveau_signalement, name='nouveau_signalement'),
# ]

from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('nouveau/', views.nouveau_signalement, name='nouveau_signalement'),
    path('analyse/', views.analyse, name='analyse'),
]
