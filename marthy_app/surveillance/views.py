from django.shortcuts import render, redirect
from .models import Signalement, DistrictSante
from django.db.models import Sum, Count, F, FloatField, ExpressionWrapper
from .forms import SignalementForm
import json

def dashboard(request):
    signalements = Signalement.objects.all().order_by('-date_declaration')[:10]
    total_cas = Signalement.objects.aggregate(Sum('nombre_cas'))['nombre_cas__sum'] or 0
    total_deces = Signalement.objects.aggregate(Sum('nombre_deces'))['nombre_deces__sum'] or 0
    alertes = Signalement.objects.filter(nombre_cas__gte=10).count()
    districts = DistrictSante.objects.count()

    # Taux de létalité global
    taux_letalite = round((total_deces / total_cas * 100), 1) if total_cas > 0 else 0

    # Évolution temporelle
    evolution = (
        Signalement.objects
        .values('date_evenement')
        .annotate(total_cas=Sum('nombre_cas'), total_deces=Sum('nombre_deces'))
        .order_by('date_evenement')
    )
    dates = json.dumps([str(e['date_evenement']) for e in evolution])
    cas_par_date = json.dumps([e['total_cas'] for e in evolution])
    deces_par_date = json.dumps([e['total_deces'] for e in evolution])

    # Répartition par maladie
    repartition = (
        Signalement.objects
        .values('maladie')
        .annotate(total=Sum('nombre_cas'))
    )
    maladies_labels = json.dumps([r['maladie'] for r in repartition])
    maladies_counts = json.dumps([r['total'] for r in repartition])

    context = {
        'signalements': signalements,
        'total_cas': total_cas,
        'total_deces': total_deces,
        'alertes': alertes,
        'districts': districts,
        'taux_letalite': taux_letalite,
        'dates': dates,
        'cas_par_date': cas_par_date,
        'deces_par_date': deces_par_date,
        'maladies_labels': maladies_labels,
        'maladies_counts': maladies_counts,
    }
    return render(request, 'surveillance/dashboard.html', context)


def analyse(request):
    # 1. Taux de létalité par maladie
    letalite_par_maladie = []
    for maladie_code, maladie_label in Signalement.MALADIE_CHOICES:
        qs = Signalement.objects.filter(maladie=maladie_code).aggregate(
            total_cas=Sum('nombre_cas'),
            total_deces=Sum('nombre_deces')
        )
        cas = qs['total_cas'] or 0
        deces = qs['total_deces'] or 0
        taux = round((deces / cas * 100), 2) if cas > 0 else 0
        if cas > 0:
            letalite_par_maladie.append({
                'maladie': maladie_label,
                'code': maladie_code,
                'cas': cas,
                'deces': deces,
                'taux': taux
            })
    letalite_par_maladie.sort(key=lambda x: x['taux'], reverse=True)

    # 2. Top 10 districts à risque (par total de cas)
    top_districts = (
        Signalement.objects
        .values('district__nom', 'district__region')
        .annotate(total_cas=Sum('nombre_cas'), total_deces=Sum('nombre_deces'))
        .order_by('-total_cas')[:10]
    )
    for d in top_districts:
        d['taux'] = round((d['total_deces'] / d['total_cas'] * 100), 1) if d['total_cas'] > 0 else 0
        if d['total_cas'] >= 50:
            d['risque'] = 'Élevé'
            d['risque_class'] = 'risk-high'
        elif d['total_cas'] >= 20:
            d['risque'] = 'Moyen'
            d['risque_class'] = 'risk-med'
        else:
            d['risque'] = 'Faible'
            d['risque_class'] = 'risk-low'

    # 3. Répartition par région
    regions_data = {}
    for sig in Signalement.objects.select_related('district'):
        region = sig.district.get_region_display()
        if region not in regions_data:
            regions_data[region] = {'cas': 0, 'deces': 0}
        regions_data[region]['cas'] += sig.nombre_cas
        regions_data[region]['deces'] += sig.nombre_deces

    regions_sorted = sorted(regions_data.items(), key=lambda x: x[1]['cas'], reverse=True)
    regions_labels = json.dumps([r[0] for r in regions_sorted])
    regions_cas = json.dumps([r[1]['cas'] for r in regions_sorted])
    regions_deces = json.dumps([r[1]['deces'] for r in regions_sorted])

    # 4. Évolution par maladie (pour le graphique empilé)
    maladies_evolution = {}
    for maladie_code, maladie_label in Signalement.MALADIE_CHOICES:
        qs = (
            Signalement.objects.filter(maladie=maladie_code)
            .values('date_evenement')
            .annotate(total=Sum('nombre_cas'))
            .order_by('date_evenement')
        )
        if qs.exists():
            maladies_evolution[maladie_label] = {
                'dates': [str(e['date_evenement']) for e in qs],
                'valeurs': [e['total'] for e in qs]
            }

    # 5. Statistiques globales pour les KPI
    total_cas = Signalement.objects.aggregate(Sum('nombre_cas'))['nombre_cas__sum'] or 0
    total_deces = Signalement.objects.aggregate(Sum('nombre_deces'))['nombre_deces__sum'] or 0
    taux_letalite_global = round((total_deces / total_cas * 100), 1) if total_cas > 0 else 0
    nb_maladies_actives = Signalement.objects.values('maladie').distinct().count()
    districts_en_alerte = Signalement.objects.filter(nombre_cas__gte=10).values('district').distinct().count()

    context = {
        'letalite_par_maladie': letalite_par_maladie,
        'top_districts': top_districts,
        'regions_labels': regions_labels,
        'regions_cas': regions_cas,
        'regions_deces': regions_deces,
        'maladies_evolution': json.dumps(maladies_evolution),
        'total_cas': total_cas,
        'total_deces': total_deces,
        'taux_letalite_global': taux_letalite_global,
        'nb_maladies_actives': nb_maladies_actives,
        'districts_en_alerte': districts_en_alerte,
    }
    return render(request, 'surveillance/analyse.html', context)


def nouveau_signalement(request):
    if request.method == 'POST':
        form = SignalementForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = SignalementForm()
    return render(request, 'surveillance/formulaire_cas.html', {'form': form})