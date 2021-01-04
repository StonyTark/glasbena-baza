import baza
import sqlite3

conn = sqlite3.connect('glasbenaBaza.db')
baza.ustvari_bazo_ce_ne_obstaja(conn)
conn.execute('PRAGMA foreign_keys = ON')

oseba,zanr,artist,zalozba,izdaja,spada,track,vloga,je_clan,je_sodeloval,je_avtor=baza.pripravi_tabele(conn)

#
#OSNOVNE TABELE
#

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
            self.id = oseba.dodaj_vrstico(ime=self.ime,priimek=self.priimek,datumRojstva=self.datumRojstva, spol=self.spol, drzava=self.drzava)
    


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
            self.id = zanr.dodaj_vrstico(imeZanra=self.ime)

class Artist:

    def __init__(self, ime, leto_nastanka, drzava, mesto, *, id=None):
        """
        Konstruktor umetniškega akta.
        """
        self.id = id
        self.ime = ime
        self.leto_nastanka = leto_nastanka
        self.drzava = drzava
        self.mesto = mesto
    
    def __str__(self):
        return "Artist: {}".format(self.ime)
    
    def dodaj_v_bazo(self):
        assert self.id is None
        with conn:
            self.id = artist.dodaj_vrstico(ime=self.ime,leto_nastanka=self.leto_nastanka,drzava=self.drzava, mesto=self.mesto)
    
    def dodaj_clane(self,clani):
        '''
        clani naj bo tabela oseb
        podane osebe nato zapiše v tabelo je_clan z trenutni artist idjem
        '''
        with conn:
            for clan in clani:
                je_clan.dodaj_vrstico(idOseba=clan.id,idArtist=self.id)
    
    @staticmethod
    def poisci(niz):
        sql = "SELECT ime,leto_nastanka,drzava,mesto FROM Artist WHERE ime LIKE ?;"
        for ime,leto_nastanka,drzava,mesto in conn.execute(sql, ['%' + niz + '%']):
            yield Artist(ime,leto_nastanka,drzava,mesto)



class Zalozba:

    def __init__(self, ime, drzava, *, id=None):
        """
        Konstruktor zalozbe.
        """
        self.id = id
        self.ime = ime
        self.drzava = drzava
    
    def __str__(self):
        return "{} , {} (id:{})".format(self.ime,self.drzava,self.id)

    def dodaj_v_bazo(self):
        assert self.id is None
        with conn:
            self.id = zalozba.dodaj_vrstico(ime=self.ime,drzava=self.drzava)


class Izdaja:

    def __init__(self, naslov, leto_izida, tip, celotnaDolzina=None ,idZalozbe=None, *, id=None):
        """
        Konstruktor izdaje.
        celotna dolzina se lahko tudi poračuna glede na tracke ?
        """
        self.id = id
        self.naslov = naslov
        self.leto_izida = leto_izida
        self.tip = tip
        self.celotnaDolzina = celotnaDolzina
        self.idZalozbe = idZalozbe
    
    def __str__(self):
        return "{}, ({})".format(self.naslov,self.leto_izida)
    
    def dodaj_v_bazo(self):
        assert self.id is None
        with conn:
            self.id = artist.dodaj_vrstico(naslov=self.naslov,leto_izida=self.leto_izida,tip=self.tip, celotnaDolzina=self.celotnaDolzina, idZalozbe=self.idZalozbe)


class Track:

    def __init__(self, naslov, dolzina, idIzdaja, *, id=None):
        """
        Konstruktor pesmi.
        """
        self.id = id
        self.naslov = naslov
        self.dolzina = dolzina
        self.idIzdaja = idIzdaja
    
    def __str__(self):
        return "{} , {}".format(self.naslov,self.idIzdaja,self.id)

    def dodaj_v_bazo(self):
        assert self.id is None
        with conn:
            self.id = track.dodaj_vrstico(naslov=self.naslov,dolzina=self.dolzina,idIzdaja=self.idIzdaja)
    
class Vloga:

    def __init__(self, naziv, *, id=None):
        """
        Konstruktor vloge.
        """
        self.id = id
        self.naziv = naziv
    
    def __str__(self):
        return "{} , {}".format(self.id,self.naziv)

    def dodaj_v_bazo(self):
        assert self.id is None
        with conn:
            self.id = vloga.dodaj_vrstico(naziv=self.naziv)

'''
def najdi(id):
        sql = """
            SELECT idOseba,ime,priimek,datumRojstva,spol,drzava
            FROM Oseba
            WHERE idOseba=?
        """
        idOseba,ime,priimek,datumRojstva,spol,drzava=conn.execute(sql,str(id)).fetchone()
        return Oseba(ime,priimek,datumRojstva,spol,drzava,id=idOseba)

osebe=[]
for i in range(5,10):
    osebe.append(najdi(i))'''


#skupina=Artist('neki',2005,'France','Paris')
#skupina.dodaj_v_bazo()
#skupina.dodaj_clane(osebe)






#test=Oseba('Geezer','Butler','1949-07-17','M','United Kingdom')
#test.dodaj_v_bazo()
#print(test)

# test=Zanr('Rock')
# test.dodaj_v_bazo()

# test=Zanr('Funk')
# test.dodaj_v_bazo()

# test=Zanr('Rock')
# test.dodaj_v_bazo()
    








