# -*- coding: utf-8 -*-
import json
from django.core.management.base import BaseCommand
from scrapy.spiders import Spider
from scrapy.http.request import Request
from scrapy.utils.project import get_project_settings
from scrapy.crawler import CrawlerProcess
from scrapy.item import Item, Field
from django.conf import settings as django_settings

class OddajaItem(Item):
    id = Field()
    ime = Field()
    opis = Field()
    link = Field()
    
    program = Field()
    tip = Field()
    
    image_urls = Field()
    images = Field()
    
class Command(BaseCommand):
    help = 'Pocohaj api.rtvslo.si za oddajami'

    def handle(self, *args, **options):
        settings = get_project_settings()
        settings.update({
            'FEED_FORMAT': 'jsonlines',
            'FEED_URI': 'file:///'+django_settings.MEDIA_ROOT +'/%(name)s/oddaje.json',
            'ITEM_PIPELINES': {'scrapy.pipelines.images.ImagesPipeline': 1},
            'IMAGES_STORE' :django_settings.MEDIA_ROOT+"/oddaje",
        
            #'LOG_ENABLED':False
            #'LOG_FILE':'loger.log',
            'LOG_LEVEL':'INFO',
        })

        process = CrawlerProcess(settings)
        process.crawl(RTVSLOOddajeSpider)
        process.start()

class RTVSLOOddajeSpider(Spider):
    name = "RTVSLO_oddaje"
    
    def start_requests(self):
        return [Request("http://api.rtvslo.si/ava/getShows?client_id=82013fb3a531d5414f478747c1aca622",callback=self.parse_oddaje)]
            
    def parse_oddaje(self,response):
        json_content = json.loads(response.body_as_unicode())

        recordings = json_content['response']
        
        for record in recordings:
            oddaja = OddajaItem()
            oddaja['id'] = record.get('id')
            oddaja['ime'] = record.get('title')
            oddaja['tip'] = record.get('showType')
            oddaja['program'] = record.get('source',"").lower()
            oddaja['link'] = record.get('link')
            
            slika_url = record['images']['thumb'].encode('utf8')
            oddaja['image_urls'] = [slika_url]
            
            opis = record.get('description')
            if opis:
                oddaja['opis'] = opis
            else:
                opis = record.get('broadcast',{}).get("description","")
                oddaja['opis'] = opis
                
            yield oddaja