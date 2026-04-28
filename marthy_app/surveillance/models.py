from django.db import models

class DistrictSante(models.Model):
    # Liste des régions du Cameroun sans espaces parasites
    NOM_REGION_CHOICES = [
        ('AD', 'Adamaoua'),
        ('CE', 'Centre'),
        ('EN', 'Extrême-Nord'),
        ('ES', 'Est'),
        ('LT', 'Littoral'),
        ('NO', 'Nord'),
        ('NW', 'Nord-Ouest'),
        ('OU', 'Ouest'),
        ('SU', 'Sud'),
        ('SW', 'Sud-Ouest'),
    ]
    
    nom = models.CharField(max_length=100, unique=True)
    # max_length=5 donne une marge de sécurité pour les codes de région
    region = models.CharField(max_length=5, choices=NOM_REGION_CHOICES)

    def __str__(self):
        return f"{self.nom} ({self.get_region_display()})"

    class Meta:
        verbose_name = "District de Santé"
        verbose_name_plural = "Districts de Santé"

class Signalement(models.Model):
    # Liste des maladies surveillées au Cameroun
    MALADIE_CHOICES = [
        ('CHOLERA', 'Choléra'),
        ('MALARIA', 'Malaria'),
        ('ROUGEOLE', 'Rougeole'),
        ('FIEVRE_JAUNE', 'Fièvre Jaune'),
        ('COVID19', 'COVID-19'),
        ('POLIO', 'Poliomyélite'),
    ]

    district = models.ForeignKey(DistrictSante, on_delete=models.CASCADE)
    maladie = models.CharField(max_length=50, choices=MALADIE_CHOICES)
    # PositiveIntegerField garantit que les nombres ne sont jamais négatifs
    nombre_cas = models.PositiveIntegerField(default=0)
    nombre_deces = models.PositiveIntegerField(default=0)
    date_evenement = models.DateField()
    # Enregistre automatiquement la date de création dans le système
    date_declaration = models.DateTimeField(auto_now_add=True)
    
    # Champ de texte libre pour les détails supplémentaires
    commentaire = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.maladie} - {self.district.nom} ({self.date_evenement})"

    class Meta:
        ordering = ['-date_declaration']