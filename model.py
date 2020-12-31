import baza
import sqlite3

conn = sqlite3.connect('glasbenaBaza.db')
baza.ustvari_bazo_ce_ne_obstaja(conn)
conn.execute('PRAGMA foreign_keys = ON')

oseba,zanr=baza.pripravi_tabele(conn)

class Oseba:

    def __init__(self, ime, priimek, datumRojstva, spol, drzava, *, id=None):
        """
        Konstruktor osebe.
        """
        self.id = id
        self.ime = ime
        self.priimek = priimek
        self.datumRojstva = datumRojstva
        self.spol = spol
        self.drzava = drzava
    
    def __str__(self):
        return "{} {} (id:{})".format(self.ime,self.priimek,self.id)
    
    def dodaj_v_bazo(self):
        assert self.id is None
        with conn:
            self.id = oseba.dodaj_vrstico(ime=self.ime,priimek=self.priimek,datumRojstva=self.datumRojstva, spol=self.datumRojstva, drzava=self.drzava)


class Zanr:

    def __init__(self, ime, *, id=None):
        """
        Konstruktor zanra.
        """
        self.id = id
        self.ime = ime
    
    def __str__(self):
        return "{} {}".format(self.id,self.ime)

    def dodaj_v_bazo(self):
        assert self.id is None
        with conn:
            self.id = oseba.dodaj_vrstico(imeZanra=self.ime)


test=Oseba('Geezer','Butler','1949-07-17','M','United Kingdom')
test.dodaj_v_bazo()
print(test)
    








