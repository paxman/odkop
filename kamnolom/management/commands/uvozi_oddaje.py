# -*- coding: utf-8 -*-
import json
from django.core.management.base import BaseCommand

from kamnolom.management.commands.pocohaj_oddaje import RTVSLOOddajeSpider
from kamnolom.models import Oddaja,Program,Tip
from django.conf import settings as django_settings

class Command(BaseCommand):
    help = 'Uvozi oddaje iz scrapy jsonlines cohanja'

    def handle(self, *args, **options):
        Oddaja.objects.all().delete()
        
        datoteka = django_settings.MEDIA_ROOT +'/'+ RTVSLOOddajeSpider.name +'/oddaje.json'
        
        with open(datoteka,'rb') as f:
            for line in f.readlines():
                data = json.loads(line)
                oddaja, created = Oddaja.objects.get_or_create(id = data['id']) 
                    
                if created:
                    oddaja.ime = data.get('ime')
                    oddaja.opis = data.get('opis')
                    oddaja.povezava = data.get('link')
                    
                    type_id = data.get('tip')
                    
                    if type_id:
                        oddaja.tip, created = Tip.objects.get_or_create(id=type_id)
                    program = data.get('program',"").lower()
                    if program:
                        oddaja.program,created = Program.objects.get_or_create(id=program)
                    
                    slika = data.get('images')
                    if len(slika) > 0:
                        slika = slika[0].get('path')
                        if slika:
                            oddaja.slika = oddaja.slika.field.generate_filename(oddaja,slika)
                    oddaja.save()