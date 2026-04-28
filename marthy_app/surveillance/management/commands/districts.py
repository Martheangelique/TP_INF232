from django.core.management.base import BaseCommand
from surveillance.models import DistrictSante

class Command(BaseCommand):
    help = 'Remplit la base de données avec les districts de santé du Cameroun'

    def handle(self, *args, **kwargs):
        # Format : (Nom du District, Code Région)
        districts = [
            # ADAMAOUA
            ('Ngaoundéré Urbain', 'AD'), ('Ngaoundéré Rural', 'AD'), ('Banyo', 'AD'), ('Tibati', 'AD'), ('Meiganga', 'AD'),
            # CENTRE
            ('Cité Verte', 'CE'), ('Djoungolo', 'CE'), ('Biyem-Assi', 'CE'), ('Mfou', 'CE'), ('Obala', 'CE'), ('Nkolbisson', 'CE'),
            # LITTORAL
            ('Deido', 'LT'), ('Nylon', 'LT'), ('Logbaba', 'LT'), ('Bonassama', 'LT'), ('Edéa', 'LT'), ('Nkongsamba', 'LT'),
            # EXTRÊME-NORD
            ('Maroua 1', 'EN'), ('Maroua 2', 'EN'), ('Kousseri', 'EN'), ('Mokolo', 'EN'), ('Yagoua', 'EN'),
            # OUEST
            ('Bafoussam', 'OU'), ('Mbouda', 'OU'), ('Dschang', 'OU'), ('Foumban', 'OU'), ('Bangangté', 'OU'),
            # NORD
            ('Garoua 1', 'NO'), ('Garoua 2', 'NO'), ('Guider', 'NO'), ('Poli', 'NO'),
            # SUD
            ('Ebolowa', 'SU'), ('Sangmélima', 'SU'), ('Kribi', 'SU'), ('Ambam', 'SU'),
            # EST
            ('Bertoua', 'ES'), ('Batouri', 'ES'), ('Abong-Mbang', 'ES'),
            # NORD-OUEST
            ('Bamenda', 'NW'), ('Kumbo', 'NW'), ('Wum', 'NW'),
            # SUD-OUEST
            ('Buea', 'SW'), ('Limbe', 'SW'), ('Kumba', 'SW'), ('Mamfe', 'SW'),
        ]

        self.stdout.write("Initialisation des districts de santé...")

        created_count = 0
        for nom, code_reg in districts:
            # get_or_create évite de recréer si vous lancez le script 2 fois
            obj, created = DistrictSante.objects.get_or_create(
                nom=nom,
                defaults={'region': code_reg}
            )
            if created:
                created_count += 1

        # CORRECTION : cette ligne était hors de la méthode (mauvaise indentation)
        self.stdout.write(self.style.SUCCESS(f"Succès ! {created_count} districts ajoutés à la base."))