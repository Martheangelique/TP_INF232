from django import forms
from .models import Signalement
from django.utils import timezone

class SignalementForm(forms.ModelForm):
    class Meta:
        model = Signalement
        fields = ['district', 'maladie', 'nombre_cas', 'nombre_deces', 'date_evenement', 'commentaire']
        widgets = {
            'date_evenement': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'district': forms.Select(attrs={'class': 'form-select'}),
            'maladie': forms.Select(attrs={'class': 'form-select'}),
            'nombre_cas': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
            'nombre_deces': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
            'commentaire': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def clean(self):
        cleaned_data = super().clean()
        nombre_cas = cleaned_data.get("nombre_cas")
        nombre_deces = cleaned_data.get("nombre_deces")
        date_evenement = cleaned_data.get("date_evenement")

        # Vérification de la date
        if date_evenement and date_evenement > timezone.now().date():
            self.add_error('date_evenement', "La date ne peut pas etre dans le futur.")

        # Vérification de la cohérence Cas/Decès
        if nombre_cas is not None and nombre_deces is not None:
            if nombre_deces > nombre_cas:
                raise forms.ValidationError(
                    "Erreur : Le nombre de deces ne peut pas etre superieur au nombre de cas."
                )
        return cleaned_data