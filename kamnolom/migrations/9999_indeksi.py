# -*- coding: utf-8 -*-
# XXX this is actually useful for very special use cases, e.g. misspel suggestions:
#  https://www.postgresql.org/docs/9.6/static/pgtrgm.html#AEN180626
from __future__ import unicode_literals

from django.db import migrations
from django.contrib.postgres.operations import TrigramExtension

class Migration(migrations.Migration):
    
    dependencies = [
        ('kamnolom','0010_posnetek_podnapisi')
    ]
    
    operations = [
        TrigramExtension(),
        migrations.RunSQL(
            'CREATE INDEX izsek_gin_idx ON kamnolom_izsek USING gin (upper(vsebina) gin_trgm_ops);',
            reverse_sql='drop index izsek_gin_idx;'
        ),
        migrations.RunSQL(
            'CREATE INDEX posnetek_naslov_gin_idx ON kamnolom_posnetek USING gin (upper(naslov) gin_trgm_ops);',
            reverse_sql='drop index posnetek_naslov_gin_idx;'
        ),
        migrations.RunSQL(
            'CREATE INDEX posnetek_datum_idx ON kamnolom_posnetek (datum);',
            reverse_sql='drop index posnetek_datum_idx;'
        ),
        migrations.RunSQL(
            'CREATE INDEX posnetek_dolzina_idx ON kamnolom_posnetek (dolzina);',
            reverse_sql='drop index posnetek_dolzina_idx;'
        ),
    ]