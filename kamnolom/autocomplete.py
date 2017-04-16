from dal_select2.views import Select2QuerySetView
from models import Oddaja, Program, Tip

class OddajaAutocomplete(Select2QuerySetView):
    model = Oddaja
    
    def get_queryset(self):
        qs = Oddaja.objects.all()

        if self.q:
            qs = qs.filter(ime__icontains=self.q).order_by('-ime')[:10]
        
        return qs

class TipAutocomplete(Select2QuerySetView):
    model = Tip
    
    def get_queryset(self):
        qs = Tip.objects.all()

        if self.q:
            qs = qs.filter(ime__icontains=self.q).order_by('-ime')[:10]
        
        return qs

class ProgramAutocomplete(Select2QuerySetView):
    model = Program
    
    def get_queryset(self):
        qs = Program.objects.all()

        if self.q:
            qs = qs.filter(ime__icontains=self.q).order_by('-ime')[:10]
        
        return qs
    