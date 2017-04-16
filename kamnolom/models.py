from __future__ import unicode_literals

from os.path import join

from django.db import models
from django.db.models.deletion import DO_NOTHING
from django.utils.safestring import mark_safe
from django.conf import settings

class Program(models.Model):
    id = models.TextField(primary_key=True)
    ime = models.TextField()
    
    def __repr__(self):
        if self.ime:
            return self.ime
        
        return u"Neznano"
    
    def __str__(self):
        return self.__repr__()
    
    def __unicode__(self):
        return self.__repr__()
    
class Tip(models.Model):
    id = models.IntegerField(primary_key=True)
    ime = models.TextField()

    def __repr__(self):
        if self.ime:
            return self.ime
        
        return u"Neznano"
    
    def __str__(self):
        return self.__repr__()
    
    def __unicode__(self):
        return self.__repr__()
    
class Oddaja(models.Model):
    id = models.IntegerField(primary_key=True)
    ime = models.TextField(null=True,blank=True)
    opis = models.TextField(null=True,blank=True)
    povezava = models.URLField(null=True,blank=True)
    slika = models.ImageField(upload_to='oddaje', null=True,blank=True)
    
    program = models.ForeignKey(Program,null=True,blank=True)
    tip = models.ForeignKey(Tip,null=True,blank=True)
    
    def predogledna_slika(self):
        if self.slika:
            absolute_url = join(settings.MEDIA_URL, self.slika.url)
            return mark_safe('<img src="%s" width="150" height="150" />' % absolute_url)
        return u""
    
    predogledna_slika.short_description = u"Slika"
    
    def __repr__(self):
        return self.ime
    
    def __str__(self):
        return self.__repr__()
    
    def __unicode__(self):
        return self.__repr__()
    
class Posnetek(models.Model):
    id = models.IntegerField(primary_key=True)
    naslov = models.TextField(null=True,blank=True)
    povezava_4d = models.URLField(null=True,blank=True)
    #slika = models.ImageField(null=True,blank=True) 
    datum = models.DateField(null=True,blank=True)
    dolzina = models.TimeField(null=True,blank=True)
    
    podnapisi = models.FileField(upload_to='podnapisi',null=True,blank=True)
    
    oddaja = models.ForeignKey(Oddaja,null=True,blank=True)
    
    #def predogled_slika(self):
    #    absolute_url = join(settings.MEDIA_URL, self.slika.url)
    #    return mark_safe('<img src="%s" width="150" height="150" />' % absolute_url)

    #predogled_slika.short_description = u"Slika"
    
    def __repr__(self):
        return self.naslov
    
    def __str__(self):
        return self.__repr__()
    
    def __unicode__(self):
        return self.__repr__()
    
class Izsek(models.Model):
    vsebina = models.TextField(null=True,default="")
    zacetek = models.TimeField(null=True,blank=True)
    konec = models.TimeField(null=True,blank=True)
    
    posnetek = models.ForeignKey(Posnetek,null=True,blank=True, on_delete=DO_NOTHING)
    
    def __repr__(self):
        return self.naslov
    
    def __str__(self):
        return self.__repr__()
    
    def __unicode__(self):
        return self.__repr__()