import baza
import sqlite3

conn = sqlite3.connect('glasbenaBaza.db')
baza.ustvari_bazo_ce_ne_obstaja(conn)
conn.execute('PRAGMA foreign_keys = ON')

oseba,zanr,artist,zalozba,izdaja,spada,track,vloga,je_clan,je_sodeloval,je_avtor=baza.pripravi_tabele(conn)

#
#OSNOVNE TABELE
#

def enkapsulirajNiz(niz):
    return '%' + niz + '%'

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
    
    def clan(self):
        rez=[]
        sql = "SELECT a.idArtist, a.ime FROM Artist a JOIN je_clan j ON j.idArtist=a.idArtist WHERE j.idOseba=? ORDER BY a.ime;"
        poizv=conn.execute(sql,[self.id,])
        for vrst in poizv.fetchall():
            rez.append(tuple(vrst))
        
        return rez

    def relevantnaDela(self):
        rez=[]
        sql="SELECT FROM Je_Sodeloval WHERE idOseba=?"
        poizv=conn.execute(sql,[self.id,])
        for vrst in poizv.fetchall():
            rez.append(vrst(0))
        return rez
    
    @staticmethod
    def brisiID(id):
        with conn:
            #Brisi iz vmesnih
            sql="DELETE FROM Je_Sodeloval WHERE idOseba=?"
            poizv=conn.execute(sql,[id,])

            sql="DELETE FROM Je_Clan WHERE idOseba=?"
            poizv=conn.execute(sql,[id,])

            #Brisi iz glavne
            sql="DELETE FROM Oseba WHERE idOseba=?"
            poizv=conn.execute(sql,[id,])

    @staticmethod
    def poisci_po_ImePriimek(**kwargs):
        ime=kwargs['ime']
        priimek=kwargs['priimek']
        sql = "SELECT idOseba,ime,priimek,datumRojstva,spol,drzava FROM Oseba WHERE ime LIKE ? AND priimek LIKE ? ORDER BY priimek;"
        for osID,ime,priimek,datumRojstva,spol,drzava in conn.execute(sql, ['%' + ime + '%','%' + priimek + '%']):
            yield Oseba(ime,priimek,datumRojstva,spol,drzava,id=osID)
    
    @staticmethod
    def poisci_po_vsem(ime,priimek,dat_od,dat_do,spol,drzava):
        sql = '''SELECT idOseba,ime,priimek,datumRojstva,spol,drzava FROM Oseba 
                WHERE ime LIKE ? AND priimek LIKE ? AND (datumRojstva BETWEEN ? AND ?) AND spol LIKE ? AND drzava LIKE ?
                ORDER BY lower(priimek);
        '''
        for osID,ime,priimek,datumRojstva,spol,drzava in conn.execute(sql, [enkapsulirajNiz(ime),enkapsulirajNiz(priimek),dat_od,dat_do,enkapsulirajNiz(spol),enkapsulirajNiz(drzava)]):
            yield Oseba(ime,priimek,datumRojstva,spol,drzava,id=osID)

    @staticmethod
    def poisciID(id):
        sql = "SELECT ime,priimek,datumRojstva,spol,drzava FROM Oseba WHERE idOseba= ?;"
        rez=conn.execute(sql, [id,])
        ime,priimek,datumRojstva,spol,drzava=rez.fetchone()
        return Oseba(ime,priimek,datumRojstva,spol,drzava,id=id)
    
    @staticmethod
    def vrni_spisek_oseb():
        sql = "SELECT idOseba,ime,priimek,datumRojstva FROM Oseba ORDER BY lower(priimek);"
        poizv=conn.execute(sql)
        rez=[]
        for vrst in poizv.fetchall():
            rez.append(tuple(vrst))
        return rez
    
    @staticmethod
    def dummy():
        return Oseba(None,None,None,None,None)
    
    


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
    
    @staticmethod
    def vrni_zanre():
        #Metoda vrne spisek trenutno zapisanih žanrov v obliki tabele
        sql='SELECT idZanr, imeZanra FROM Zanr'
        rez=[]
        poizv=conn.execute(sql)
        for vrst in poizv.fetchall():
            rez.append(tuple(vrst))
        return rez
    
    @staticmethod
    def dummy():
        return Zanr(None)


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
        clani naj bo tabela ID-jev željenih članov
        podane osebe nato zapiše v tabelo je_clan z trenutni artist idjem
        '''
        with conn:
            for clanID in clani:
                je_clan.dodaj_vrstico(idOseba=clanID,idArtist=self.id)
    
    def dodaj_izdajo(self,idIzdaje):
        '''
        Trenutnega artista označi kot avtorja podane izdaje
        '''
        je_avtor.dodaj_vrstico(idIzdaje=idIzdaje,idArtist=self.id)
    
    def vrni_clane(self):
        rez=[]
        sql = '''SELECT o.idOseba, o.ime, o.priimek FROM Oseba o 
                JOIN Je_Clan j ON j.idOseba=o.idOseba
                WHERE j.idArtist=?;'''
        poizv=conn.execute(sql,[self.id,])
        for vrst in poizv.fetchall():
            rez.append(tuple(vrst))
        return rez
    
    def vrni_izdaje(self):
        rez=[]
        sql = '''
            SELECT i.idIzdaja,i.naslov,i.leto_izida FROM Izdaja i
            JOIN Je_Avtor j ON i.idIzdaja=j.idIzdaja
            WHERE j.idArtist=?
            ORDER BY i.leto_izida;
        '''
        poizv=conn.execute(sql,[self.id,])
        for vrst in poizv.fetchall():
            rez.append(tuple(vrst))
        return rez
    
    def vrni_neClane(self):
        rez=[]
        sql = '''SELECT DISTINCT idOseba, ime, priimek,datumRojstva FROM Oseba
        WHERE idOseba NOT IN (SELECT idOseba FROM je_clan WHERE idArtist=?);'''
        poizv=conn.execute(sql,[self.id,])
        for vrst in poizv.fetchall():
            rez.append(tuple(vrst))
        return rez

    @staticmethod
    def poisci_po_imenu(niz):
        sql = "SELECT idArtist,ime,leto_nastanka,drzava,mesto FROM Artist WHERE ime LIKE ? ORDER BY ime;"
        for arID,ime,leto_nastanka,drzava,mesto in conn.execute(sql, ['%' + niz + '%']):
            yield Artist(ime,leto_nastanka,drzava,mesto,id=arID)
    

    @staticmethod
    def poisci_po_vsem(ime,leto_od,leto_do,drzava,mesto):
        sql = '''SELECT idArtist,ime,leto_nastanka,drzava,mesto FROM Artist 
                WHERE ime LIKE ? AND (leto_nastanka BETWEEN ? AND ?) AND drzava LIKE ? AND mesto LIKE ?
                ORDER BY lower(ime);

        '''
        for arID,ime,leto_nastanka,drzava,mesto in conn.execute(sql, [enkapsulirajNiz(ime),leto_od,leto_do,enkapsulirajNiz(drzava),enkapsulirajNiz(mesto)]):
            yield Artist(ime,leto_nastanka,drzava,mesto,id=arID)
    
    @staticmethod
    def poisciID(id):
        sql = "SELECT ime,leto_nastanka,drzava,mesto FROM Artist WHERE idArtist= ?;"
        rez=conn.execute(sql, [id,])
        ime,leto_nastanka,drzava,mesto=rez.fetchone()
        return Artist(ime,leto_nastanka,drzava,mesto,id=id)
    
    @staticmethod
    def vrni_spisek_artistov():
        sql = "SELECT idArtist,ime,drzava FROM Artist ORDER BY ime;"
        poizv=conn.execute(sql)
        rez=[]
        for vrst in poizv.fetchall():
            rez.append(tuple(vrst))
        return rez

    @staticmethod
    def dummy():
        return Artist(None,None,None,None)



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

    #TODO potrebna modifikacija, ki zveže izdajo na avtorja - torej potreben še en parameter v initu (al neki) , metoda, ki vrne avtorja?

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
            self.id = izdaja.dodaj_vrstico(naslov=self.naslov,leto_izida=self.leto_izida, celotnaDolzina=self.celotnaDolzina, tip=self.tip, idZalozbe=self.idZalozbe)

    def vrni_Tracklist(self):
        rez=[]
        sql = '''
            SELECT idTrack,naslov,dolzina FROM Track
            WHERE idIzdaja=?
        '''
        poizv=conn.execute(sql,[self.id,])
        for vrst in poizv.fetchall():
            rez.append(tuple(vrst))
        return rez
    
    def vrni_Avtorje(self):
        rez=[]
        sql = '''
            SELECT a.idArtist,a.ime FROM Artist a
            JOIN Je_Avtor j ON j.idArtist=a.idArtist
            WHERE j.idIzdaja=?;
        '''
        poizv=conn.execute(sql,[self.id,])
        for vrst in poizv.fetchall():
            rez.append(tuple(vrst))
        return rez
    
    def vrni_Sodelujoce(self):
        rez = []
        sql = """
            SELECT o.idOseba,ime, priimek, naziv FROM OSEBA o 
            JOIN Je_Sodeloval j ON (o.idOseba = j.idOseba) 
            JOIN Vloga v ON v.idVloga=j.idVloga
            WHERE j.idIzdaja = ?
            ORDER BY naziv,priimek
        """
        poziv = conn.execute(sql, [self.id,])
        for vrst in poziv.fetchall():
            rez.append(tuple(vrst))
        return rez
    
    def dodaj_avtorje(self,avtorji):
        '''
        avtorji naj bo tabela ID-jev željenih članov
        podane osebe nato zapiše v tabelo je_clan z trenutni artist idjem
        '''
        with conn:
            for avtorID in avtorji:
                je_avtor.dodaj_vrstico(idArtist=avtorID,idIzdaja=self.id)

                "Vzame trenutne člane (osebe) in jih zapiše v je_sodeloval kot avtorje"
                temp=Artist.poisciID(avtorID).vrni_clane()
                for clan,_,_ in temp:
                    je_sodeloval.dodaj_vrstico(idOseba=clan, idIzdaja=self.id, idVloga=1) #VLOGA ZA AVTORJA NAJ BO 1
              
    def dodaj_zanr(self,zanrID):
        with conn:
            spada.dodaj_vrstico(idIzdaja=self.id,idZanr=zanrID)
    
    def vrni_zanre(self):
        rez=[]
        sql='SELECT z.idZanr,z.imeZanra FROM Zanr z JOIN Spada s ON s.idZanr=z.idZanr WHERE s.idIzdaja=?'
        poziv = conn.execute(sql, [self.id,])
        for vrst in poziv.fetchall():
            rez.append(tuple(vrst))
        return rez

    def vrni_mozne_zanre(self):
        rez=[]
        sql='SELECT idZanr,imeZanra FROM Zanr WHERE idZanr NOT IN(SELECT idZanr FROM Spada WHERE idIzdaja=?) '
        poziv = conn.execute(sql, [self.id,])
        for vrst in poziv.fetchall():
            rez.append(tuple(vrst))
        return rez

    @staticmethod
    def poisci_po_naslovu(niz):
        sql = "SELECT idIzdaja,naslov,leto_izida,celotnaDolzina,tip,idZalozbe FROM Izdaja WHERE naslov LIKE ?;"
        for izID,naslov,leto_izida,celotnaDolzina,tip,idZalozbe in conn.execute(sql, ['%' + niz + '%']):
            yield Izdaja(naslov,leto_izida,celotnaDolzina,tip,idZalozbe,id=izID)
    
    @staticmethod
    def poisci_po_vsem(naslov,leto_od,leto_do,tip):
        sql = '''SELECT idIzdaja,naslov,leto_izida,celotnaDolzina,tip,idZalozbe FROM Izdaja 
                WHERE naslov LIKE ? AND (leto_izida BETWEEN ? AND ?) AND tip LIKE ?
                ORDER BY lower(naslov);
        '''
        for izID,naslov,leto_izida,celotnaDolzina,tip,idZalozbe in conn.execute(sql, [enkapsulirajNiz(naslov),leto_od,leto_do,enkapsulirajNiz(tip)]):
            yield Izdaja(naslov,leto_izida,celotnaDolzina,tip,idZalozbe,id=izID)
    
    @staticmethod
    def poisciID(id):
        sql = "SELECT naslov,leto_izida,celotnaDolzina,tip,idZalozbe FROM Izdaja WHERE idIzdaja= ?;"
        rez=conn.execute(sql, [id,])
        naslov,leto_izida,celotnaDolzina,tip,idZalozbe=rez.fetchone()
        return Izdaja(naslov,leto_izida,tip,celotnaDolzina,idZalozbe,id=id)
    
    '''
    TODO
    Ob dodaji nove izdaje:
    -dodaj artista kot avtorja
    -trenutne clane zapisi kot avtorje v Je_sodeloval
    -v pregledu izdaje izpisi tudi je_sodeloval
    '''


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
    
    @staticmethod
    def izbrisi_ID(id):
        sql = "DELETE FROM Track WHERE idTrack=?"
        with conn:
            conn.execute(sql,[id,])
    
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
    








