from django.conf.urls import url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.views.i18n import JavaScriptCatalog

from kamnolom.views import IzsekListView,PosnetekView
from kamnolom.autocomplete import OddajaAutocomplete, TipAutocomplete, ProgramAutocomplete

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^jsi18n/$', JavaScriptCatalog.as_view(), name='javascript-catalog'),
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += [
    url(
        r'^oddaja-url/$',
        OddajaAutocomplete.as_view(),
        name='oddaja-url',
    ),
    url(
        r'^program-url/$',
        ProgramAutocomplete.as_view(),
        name='program-url',
    ),
    url(
        r'^tip-url/$',
        TipAutocomplete.as_view(),
        name='tip-url',
    ),            
    
]

urlpatterns += [
    url(r'^$$', IzsekListView.as_view(),name='domov'),
    url(r'^posnetek/(?P<pk>[0-9]+)(?:/(?P<cas>[0-9]{2}[:][0-9]{2}[:][0-9]{2}))?/$', PosnetekView.as_view(), name='posnetek-detail'),
]

#import debug_toolbar
#urlpatterns += [
#        url(r'^__debug__/', include(debug_toolbar.urls)),
#    ]