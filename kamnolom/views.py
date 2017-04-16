from django.views.generic.detail import DetailView
from django.core.paginator import Paginator
from django.utils.functional import cached_property

from django_filters.views import FilterView

from models import Izsek, Posnetek
from kamnolom.filters import IzsekFilter

#ne delatjcounta :/
class CustomPaginator(Paginator):
    
    @cached_property
    def count(self):
        return 1000
    pass

class IzsekListView(FilterView):
    model = Izsek
    paginate_by = 20
    filterset_class = IzsekFilter
    paginator_class = CustomPaginator
    
    def get_filterset_kwargs(self, filterset_class):
        kwargs = super(IzsekListView, self).get_filterset_kwargs(filterset_class)
        if kwargs['data'] is not None and 'page' in kwargs['data']:
            data = kwargs['data'].copy() ; del data['page']
            kwargs['data'] = data
        return kwargs

class PosnetekView(DetailView):
    model = Posnetek
    
    def get_context_data(self, **kwargs):
        context = DetailView.get_context_data(self, **kwargs)
        if self.kwargs.get('cas',None):
            context.update({'cas':self.kwargs.get('cas',None)})
        
        return context