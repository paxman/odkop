# -*- coding: utf-8 -*-
import json
from django.core.management.base import BaseCommand
from datetime import datetime

from scrapy.spiders import Spider
from scrapy.http.request import Request
from scrapy.utils.project import get_project_settings
from scrapy.crawler import CrawlerProcess
from scrapy.item import Item, Field
from django.conf import settings as django_settings

STEP = 500
FIRST = "http://api.rtvslo.si/ava/getSearch?client_id=82013fb3a531d5414f478747c1aca622&sort=date&order=asc&pageSize={step}&pageNumber={page}&subtitled=1"
RECORDING = "http://api.rtvslo.si/ava/getRecording/{id}?client_id=82013fb3a531d5414f478747c1aca622"

class PosnetekItem(Item):
    id = Field()
    naslov = Field()
    povezava_4d = Field()
    #slika = Field() 
    datum = Field()
    dolzina = Field()

    oddaja = Field()
    
    file_urls = Field()
    files = Field()

class Command(BaseCommand):
    help = 'Pocohaj api.rtvslo.si za posnetki s podnapisi'

    def handle(self, *args, **options):
        settings = get_project_settings()
        settings.update({
            'FEED_FORMAT': 'jsonlines',
            'FEED_URI': 'file:///'+django_settings.MEDIA_ROOT +'/%(name)s/posnetki.json',
            'ITEM_PIPELINES' : {'scrapy.pipelines.files.FilesPipeline': 1},
            'FILES_STORE' : django_settings.MEDIA_ROOT+"/podnapisi",
            
            #'LOG_FILE':'loger.log',
            #'LOG_ENABLED':False
            'LOG_LEVEL':'INFO',
        })

        process = CrawlerProcess(settings)
        process.crawl(RTVSLOPosnetkiSpider)
        process.start()

class RTVSLOPosnetkiSpider(Spider):
    name = "RTVSLO_posnetki"
    
    STEP = 500
    FIRST = "http://api.rtvslo.si/ava/getSearch?client_id=82013fb3a531d5414f478747c1aca622&sort=date&order=asc&pageSize={step}&pageNumber={page}&subtitled=1"
    RECORDING = "http://api.rtvslo.si/ava/getRecording/{id}?client_id=82013fb3a531d5414f478747c1aca622"
    
    def start_requests(self):
        return [Request(FIRST.format(step=STEP,page=0),callback=self.parse_initial,dont_filter=True)]
            
    def parse_initial(self,response):
        json_content = json.loads(response.body_as_unicode())
        hits = json_content['response']['meta']['hits']
     
        pages = int(hits/STEP)
        
        for page in range(0,pages+1):
            url = FIRST.format(step=STEP,page=page)
            yield Request(url,callback=self.parse_page                        )
    
    def parse_page(self,response):
        response = json.loads(response.body_as_unicode())
        recordings = response['response']['recordings']
        
        for record in recordings:
            posnetek = PosnetekItem()
            posnetek['id'] = record.get('id')
            posnetek['naslov'] = record.get('title')
            posnetek['dolzina'] = record.get('length')
            posnetek['povezava_4d'] = record.get('link')
            posnetek['oddaja'] = record.get('showId')
            
            #polomi datum
            date = record.get('date')
            if date:
                datetime_object = datetime.strptime(date, '%d.%m.%Y')
                posnetek['datum'] = datetime_object
            
            #uporabi sliko oddaje
            #posnetek['slika'] = record['images']['thumb'].encode('utf8')
            
            url = RECORDING.format(id=posnetek['id'])
       
            yield Request(url,meta={'recording':posnetek}, callback=self.parse_posnetek_subtitles_link)
            
    def parse_posnetek_subtitles_link(self,response):
        json_content = json.loads(response.body_as_unicode())
        recording = response.meta['recording']
        
        file_url = json_content['response']['subtitles'][0]['file']  
        recording['file_urls'] =[file_url]
        
        yield recording