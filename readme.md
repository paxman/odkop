Odkop - Odprti kop iz domačega naslanjača
===================

Približna lokalna kopija [Odprtega kopa](https://web.archive.org/web/20131224000705/http://www.rtvslo.si/odprtikop/o_odprtem_kopu/), ki ga je RTVSLO iz neznanega razloga [ukinil](https://rtvslo.si/odprtikop).

Zahteve
----------
 - [Python](https://www.python.org/downloads/) 
 - [PostgreSQL](https://www.postgresql.org/download/)

Namestitev
----------------
    
    #ustvarite bazo v postgres (pgadmin4 ali konzola)
    #spremenite podatke o dostopu do baze v odkop/settings.py
    
    pip install -r requirements.txt
    
    #za administracijo:
    #python manage.py createsuperuser
    
    #dodajte tabele
    python manage.py migrate
    python manage.py migrate kamnolom 0010_posnetek_podnapisi
    
    #pocohajte API
    python manage.py pocohaj_oddaje
    python manage.py pocohaj_posnetke
    
    #uvozite
    python manage.py uvozi_tip_program
    python manage.py uvozi_oddaje
    python manage.py uvozi_posnetke
    python manage.py uvozi_podnapise    
    
    #ustvarite indekse
    python manage.py migrate kamnolom
    
    #zaženite strežnik
    python manage.py runserver
    

Avtorji ikon
----------------
Gumb predvajaj: P. J. Onori, https://www.iconfinder.com/icons/118620/play_icon
Gumb preberi: P. J. Onori, https://www.iconfinder.com/icons/118614/more_read_icon
Ikona buldožerja: Freepik, http://www.flaticon.com/free-icon/bulldozer_356249

TODO
------
- FTS?
- pgtrgm word_similarity?
- boljša detekcija govorcev