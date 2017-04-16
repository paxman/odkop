# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand
from kamnolom.models import Tip,Program

class Command(BaseCommand):
    help = 'Uvozi programe in tipe oddaj'

    def handle(self, *args, **options):
        #tip
        for key,val in {'28': 'Priporočamo',
                    '29' : 'Nedefinirano',
                    '30' : 'Kulturno umetniški',
                    '31' : 'Otroški',
                    '15890838' : 'Mladinski',
                    '32' : 'Verski',
                    '33' : 'Izobraževalni',
                    '34' : 'Informativni',
                    '35' : 'Športni',
                    '36' : 'Razvedrilni',
                    '6781958' : 'Iz TV arhiva',
                    '15890837' : 'Reklame'}.iteritems():
            tip,created = Tip.objects.get_or_create(id=key)
            
            if created:
                tip.ime=val
                tip.save()
        
        #program
        for key,val in {'slo1':'TV Slovenija 1',
                        'slo2':'TV Slovenija 2',
                        'slo3':'TV Slovenija 3',
                        'tvkp':'TV Koper',
                        'tvmb':'TV Maribor',
                        'ra1':'Radio Prvi program',
                        'val202':'Radio Val202',
                        'ars':'Radio ARS',
                        'ramb':'Radio Maribor',
                        'rakp':'Radio Koper',
                        'capo':'Radio Capodistria',
                        'rsi':'Radio Si',
                        'mmr':'Radio MMR'}.iteritems():
            program,created = Program.objects.get_or_create(id=key)
            
            if created: 
                program.ime=val
                program.save()
        