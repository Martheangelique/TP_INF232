from django.shortcuts import render, redirect
from .models import Signalement, DistrictSante
from django.db.models import Sum
from .forms import SignalementForm

def dashboard(request):
    # Récupérer les données pour le template
    signalements = Signalement.objects.all().order_by('-date_declaration')[:10]
    total_cas = Signalement.objects.aggregate(Sum('nombre_cas'))['nombre_cas__sum'] or 0
    total_deces = Signalement.objects.aggregate(Sum('nombre_deces'))['nombre_deces__sum'] or 0
    alertes = Signalement.objects.filter(nombre_cas__gte=10).count()
    districts = DistrictSante.objects.count()

    context = {
        'signalements': signalements,
        'total_cas': total_cas,
        'total_deces': total_deces,
        'alertes': alertes,
        'districts': districts,
    }
    return render(request, 'surveillance/dashboard.html', context)

def nouveau_signalement(request):
    if request.method == 'POST':
        form = SignalementForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = SignalementForm()
    return render(request, 'surveillance/formulaire_cas.html', {'form': form})