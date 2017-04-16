from django.core.paginator import Paginator
from django.utils.functional import cached_property

class CustomPaginator(Paginator):
    
    @cached_property
    def count(self):
        return 1000
        #return Paginator.count(self)
    pass
