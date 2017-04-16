from django_filters.filterset import FilterSet
from django_filters.filters import CharFilter, DateFromToRangeFilter,\
    OrderingFilter
from dal_select2.widgets import ListSelect2
from kamnolom.widgets import RangePickerWidget
from kamnolom.models import Izsek,Posnetek

class IzsekFilter(FilterSet):

    naslov = CharFilter(name='posnetek',lookup_expr='naslov__icontains',label="Naslov",help_text="")
    vsebina = CharFilter(name='vsebina',lookup_expr='icontains',label="Vsebina",help_text="")
    
    datum = DateFromToRangeFilter(name='posnetek__datum',widget=RangePickerWidget(),label="Datum",help_text="")
    
    oddaja = CharFilter(name='posnetek__oddaja',widget=ListSelect2(url='oddaja-url'),label="Oddaja",help_text="")    
    tip_oddaje = CharFilter(lookup_expr='posnetek__oddaja__tip',widget=ListSelect2(url='tip-url'),label="Tip oddaje",help_text="")
    program = CharFilter(lookup_expr='posnetek__oddaja__program',widget=ListSelect2(url='program-url'),label="S programa",help_text="")
        
    o = OrderingFilter(
         fields=(
            ('posnetek__datum', 'datum'),
            ('posnetek__dolzina', 'dolzina'),
        ),

        field_labels={
            'datum': 'Datum',
            'dolzina': 'Dolzina',
        }
    )
    
    class Meta:
        model = Izsek
        fields = {}
        order_by_field = '-posnetek__datum'

    
    def __init__(self, *args, **kwargs):
        super(IzsekFilter, self).__init__(*args, **kwargs)
        
        #ugh
        if self.data == {}:
            self.queryset = Posnetek.objects.all().order_by("-datum")
            
    @property
    def qs(self):
        qs = super(IzsekFilter, self).qs
        
        if hasattr(self.form,'cleaned_data'):
            
            value = self.form.cleaned_data.get('vsebina', None)
            
            #dovolj dobro bo
            if value:
                qs = qs.extra(
                    select={'snippet': "ts_headline('simple', \"vsebina\", plainto_tsquery(%s), 'StartSel=<span> , StopSel= </span>,MaxFragments=0,HighlightAll=TRUE')"},
                    select_params=[value,"style='background:lightblue;'"],     
                )
        return qs  
