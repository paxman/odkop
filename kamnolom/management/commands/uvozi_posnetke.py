# -*- coding: utf-8 -*-
import json
from django.core.management.base import BaseCommand

from kamnolom.management.commands.pocohaj_posnetke import RTVSLOPosnetkiSpider
from kamnolom.models import Posnetek,Oddaja
from django.conf import settings as django_settings

from datetime import datetime

class Command(BaseCommand):
    help = 'Uvozi posnetke iz scrapy jsonlines cohanja'

    def handle(self, *args, **options):
        Posnetek.objects.all().delete()
        
        datoteka = django_settings.MEDIA_ROOT +'/'+ RTVSLOPosnetkiSpider.name +'/posnetki.json'
        
        with open(datoteka,'rb') as f:
            for line in f.readlines():
                data = json.loads(line)
                posnetek, created = Posnetek.objects.get_or_create(id = data['id']) 
                
                if created:
                    posnetek.naslov = data.get('naslov')
                    posnetek.opis = data.get('opis')
                    posnetek.povezava_4d = data.get('povezava_4d')
                    posnetek.dolzina = data.get('dolzina')
                    posnetek.oddaja = Oddaja.objects.get(id=data.get('oddaja'))
                    
                    datum = data.get('datum')
                    datetime_object = datetime.strptime(datum, "%Y-%m-%d %H:%M:%S")
                    posnetek.datum = datetime_object.strftime('%Y-%m-%d')
                    
                    filename = data.get("files")
                    if len(filename) > 0:
                        filename = filename[0].get('path')
                        if filename:
                            posnetek.podnapisi = posnetek.podnapisi.field.generate_filename(posnetek,filename)
                    posnetek.save()