from django.contrib import admin
from kamnolom.models import Oddaja, Posnetek, Tip, Program, Izsek

class IzsekInline(admin.TabularInline):
    model = Izsek

class PosnetekInline(admin.TabularInline):
    model = Posnetek  
    
class PosnetekAdmin(admin.ModelAdmin):
    list_display = ('naslov', 'datum','povezava_4d')
    inlines = [
        IzsekInline,
    ]
    
class OddajaAdmin(admin.ModelAdmin):
    list_display = ('ime', 'opis', 'predogledna_slika', 'program','tip','povezava')
    inlines = [
        PosnetekInline,
    ]
    
class IzsekAdmin(admin.ModelAdmin):
    list_display = ('zacetek', 'konec', 'vsebina')

class ProgramAdmin(admin.ModelAdmin):
    list_display = ('id', 'ime')
  
class TipAdmin(admin.ModelAdmin):
    list_display = ('id', 'ime')

# Register your models here.
admin.site.register(Oddaja,OddajaAdmin)
admin.site.register(Posnetek,PosnetekAdmin)
admin.site.register(Tip,TipAdmin)
admin.site.register(Program,ProgramAdmin)
admin.site.register(Izsek,IzsekAdmin)