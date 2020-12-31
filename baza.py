PARAM_FMT = ":{}"

class Tabela:
    """
    Razred, ki predstavlja tabelo v bazi.
    Polja razreda:
    - ime: ime tabele
    - podatki: ime datoteke s podatki ali None
    """
    ime = None
    podatki = None

    def __init__(self, conn):
        """
        Konstruktor razreda.
        """
        self.conn = conn

    def ustvari(self):
        """
        Metoda za ustvarjanje tabele.
        Podrazredi morajo povoziti to metodo.
        """
        raise NotImplementedError

    def izbrisi(self):
        """
        Metoda za brisanje tabele.
        """
        self.conn.execute("DROP TABLE IF EXISTS {};".format(self.ime))

    def uvozi(self, encoding="UTF-8"):
        """
        Metoda za uvoz podatkov.
        Argumenti:
        - encoding: kodiranje znakov
        """
        raise NotImplementedError

    def izprazni(self):
        """
        Metoda za praznjenje tabele.
        """
        self.conn.execute("DELETE FROM {};".format(self.ime))

    def dodajanje(self, stolpci=None):
        """
        Metoda za gradnjo poizvedbe.
        Argumenti:
        - stolpci: seznam stolpcev
        """
        return "INSERT INTO {} ({}) VALUES ({});" \
            .format(self.ime, ", ".join(stolpci),
                    ", ".join(PARAM_FMT.format(s) for s in stolpci))

    def dodaj_vrstico(self, /, **podatki):
        """
        Metoda za dodajanje vrstice.
        Argumenti:
        - poimenovani parametri: vrednosti v ustreznih stolpcih
        """
        podatki = {kljuc: vrednost for kljuc, vrednost in podatki.items() if vrednost is not None}
        poizvedba = self.dodajanje(podatki.keys())
        cur = self.conn.execute(poizvedba, podatki)
        return cur.lastrowid

#
#KONKRETNE TABELE GLEDE NA ER DIAGRAM
#

#OSNOVNE TABELE
class Oseba(Tabela):
    ime='Oseba'

    def ustvari(self):
        self.conn.execute("""
            CREATE TABLE Oseba(
                idOseba INTEGER PRIMARY KEY AUTOINCREMENT,
                ime TEXT NOT NULL,
                priimek TEXT,
                datumRojstva date,
                spol INTEGER,
                drzava TEXT
            );
        """)
    
    def dodaj_vrstico(self, /, **podatki):
        return super().dodaj_vrstico(**podatki)


class Zanr(Tabela):
    ime='Zanr'

    def ustvari(self):
        self.conn.execute("""
            CREATE TABLE Zanr(
                idZanr INTEGER PRIMARY KEY AUTOINCREMENT,
                imeZanra TEXT NOT NULL
            );
        """)
    
    def dodaj_vrstico(self, /, **podatki):
        assert "imeZanra" in podatki
        cur = self.conn.execute("""
            SELECT idZanr FROM zanr
            WHERE imeZanra = :imeZanra;
        """, podatki)
        r = cur.fetchone()
        if r is None:
            return super().dodaj_vrstico(**podatki)
        else:
            id, = r
            print("Ze v bazi, ID: {}".format(str(id)))
            return id
        #return super().dodaj_vrstico(**podatki)

class Artist(Tabela):
    ime='Artist'

    def ustvari(self):
        self.conn.execute("""
            CREATE TABLE Artist(
                idArtist INTEGER PRIMARY KEY AUTOINCREMENT,
                ime TEXT NOT NULL,
                leto_nastanka INTEGER,
                drzava TEXT,
                mesto TEXT
            );
        """)
    
    def dodaj_vrstico(self, /, **podatki):
        return super().dodaj_vrstico(**podatki)

class Zalozba(Tabela):
    ime='Zalozba'

    def ustvari(self):
        self.conn.execute("""
            CREATE TABLE Zalozba(
                idZalozbe INTEGER PRIMARY KEY AUTOINCREMENT,
                ime TEXT NOT NULL,
                drzava TEXT
            );
        """)
    
    def dodaj_vrstico(self, /, **podatki):
        return super().dodaj_vrstico(**podatki)


class Izdaja(Tabela):
    ime='Izdaja'

    def ustvari(self):
        self.conn.execute("""
            CREATE TABLE Izdaja(
                idIzdaja INTEGER PRIMARY KEY AUTOINCREMENT,
                naslov TEXT NOT NULL,
                leto_izida INTEGER NOT NULL,
                celotnaDolzina time,
                tip TEXT NOT NULL,
                idZalozbe INTEGER,
                FOREIGN KEY(idZalozbe) REFERENCES Zalozba(idZalozbe)
            );
        """)
    
    def dodaj_vrstico(self, /, **podatki):
        return super().dodaj_vrstico(**podatki)


class Track(Tabela):
    ime='Track'

    def ustvari(self):
        self.conn.execute("""
            CREATE TABLE Track(
                idTrack INTEGER PRIMARY KEY AUTOINCREMENT,
                naslov TEXT NOT NULL,
                dolzina time NOT NULL,
                idIzdaja INTEGER NOT NULL,
                FOREIGN KEY (idIzdaja) REFERENCES Izdaja(idIzdaja)
            );
        """)
    
    def dodaj_vrstico(self, /, **podatki):
        return super().dodaj_vrstico(**podatki)


class Vloga(Tabela):
    ime='Vloga'

    def ustvari(self):
        self.conn.execute("""
            CREATE TABLE Vloga(
                idVloga INTEGER PRIMARY KEY AUTOINCREMENT,
                Naziv TEXT NOT NULL UNIQUE
            );
        """)
    
    def dodaj_vrstico(self, /, **podatki):
        assert "Naziv" in podatki
        cur = self.conn.execute("""
            SELECT idVloga FROM Vloga
            WHERE Naziv = :Naziv;
        """, podatki)
        r = cur.fetchone()
        if r is None:
            return super().dodaj_vrstico(**podatki)
        else:
            id, = r
            print("Ze v bazi, ID: {}".format(str(id)))
            return id


#TODO VMESNE TABELE







#USTVARJANJE BAZE

def ustvari_tabele(tabele):
    """
    Ustvari podane tabele.
    """
    for t in tabele:
        t.ustvari()

def izbrisi_tabele(tabele):
    """
    Izbriši podane tabele.
    """
    
    for t in tabele:
        t.izbrisi()


def ustvari_bazo(conn):
    """
    Izvede ustvarjanje baze.
    """
    tabele = pripravi_tabele(conn)
    izbrisi_tabele(tabele)
    ustvari_tabele(tabele)


def pripravi_tabele(conn):
    """
    Pripravi objekte za tabele.
    """
    oseba=Oseba(conn)
    zanr=Zanr(conn)
    artist=Artist(conn)
    zalozba=Zalozba(conn)
    izdaja=Izdaja(conn)
    track=Track(conn)
    vloga=Vloga(conn)
    return [oseba,zanr,artist,zalozba,izdaja,track,vloga]

def ustvari_bazo_ce_ne_obstaja(conn):
    """
    Ustvari bazo, če ta še ne obstaja.
    """
    with conn:
        cur = conn.execute("SELECT COUNT(*) FROM sqlite_master")
        if cur.fetchone() == (0, ):
            ustvari_bazo(conn)












