# -*- coding: utf-8 -*-
import re
import codecs
import nltk

from django.core.management.base import BaseCommand

from nltk.tokenize import sent_tokenize

from kamnolom.models import Posnetek, Izsek
from util import strip_tags

regex = re.compile("(?:[-–][\w]+)", re.IGNORECASE | re.UNICODE)
nltk.download(['punkt'], quiet=True)

class Command(BaseCommand):
    help = 'Uvozi posnetke iz cohanja'

    def handle(self, *args, **options):
        Izsek.objects.all().delete()
        izseki = []
        
        for posnetek in Posnetek.objects.all():
            
            if posnetek.podnapisi:
                
                file_path = posnetek.podnapisi.path
                
                vseb = codecs.open(file_path,encoding='utf-8',errors='replace').read()
                
                stripped = strip_tags(vseb) 
                #has_speakers = len(regex.findall(stripped)) > 0 
                vsebina_split = sent_tokenize(stripped,language='slovene')
                #pprint(vsebina_split)
                
                last_cas = ""
                izsek = Izsek()
                izsek.posnetek = posnetek
                
                for split in vsebina_split:
                    if split == "":
                        continue
                    
                    split = split.replace(u"WEBVTT","")
                    nov_cas = [ b.split("-->") for b in split.split('\n') if "-->" in b]
                    split_in = [ b.strip() for b in split.split('\n') if b != "" and "-->" not in b]
                    #pprint(nov_cas)
                    
                    if not last_cas:
                        nov_cas_a = nov_cas.pop(0)
                        last_cas = nov_cas_a[0]
                    
                    if not izsek.zacetek:
                        izsek.zacetek = last_cas
                        
                    sentence = " ".join(split_in).strip()
                    
                    if sentence.startswith((u"-",u"–")) or (len(sentence) + len(izsek.vsebina) > 500):
                        #if len(izsek.vsebina):
                        #    print izsek.zacetek,izsek.vsebina
                        izseki.append(izsek)
                        
                        izsek=Izsek()
                        izsek.vsebina = sentence.upper()
                        izsek.zacetek = last_cas
                        izsek.posnetek = posnetek
                    else:
                        izsek.vsebina += " "+sentence.upper()
                    
                    if nov_cas:
                        nov_cas_a = nov_cas.pop()
                        last_cas = nov_cas_a[0]
                
                if len(izsek.vsebina):         
                    izseki.append(izsek)    
                    
                    #pprint(cas)

            if len(izseki) > 10000:  
                Izsek.objects.bulk_create(izseki)       
                izseki = [] 
                        
        Izsek.objects.bulk_create(izseki)