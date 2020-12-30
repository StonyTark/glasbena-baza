CREATE TABLE Oseba(
    idOseba INTEGER PRIMARY KEY AUTOINCREMENT,
    ime TEXT NOT NULL,
    priimek TEXT,
    datumRojstva date,
    spol INTEGER,
    drzava TEXT
)

CREATE TABLE Artist(
    idArtist INTEGER PRIMARY KEY AUTOINCREMENT,
    ime TEXT NOT NULL,
    leto_nastanka INTEGER,
    drzava TEXT,
    mesto TEXT
)

CREATE TABLE Zalozba(
    idZalozbe INTEGER PRIMARY KEY AUTOINCREMENT,
    ime TEXT NOT NULL,
    drzava TEXT
)

CREATE TABLE Zanr(
    idZanr INTEGER PRIMARY KEY AUTOINCREMENT,
    imeZanra TEXT NOT NULL
)

CREATE TABLE Izdaja(
    idIzdaja INTEGER PRIMARY KEY AUTOINCREMENT,
    naslov TEXT NOT NULL,
    leto_izida INTEGER NOT NULL,
    celotnaDolzina time,
    tip TEXT NOT NULL,
    idZalozbe INTEGER NOT NULL,
    FOREIGN KEY(idZalozbe) REFERENCES Zalozba(idZalozbe)
)

CREATE TABLE Spada(
    idIzdaja INTEGER NOT NULL,
    idZanr INTEGER NOT NULL,
    FOREIGN KEY(idIzdaja) REFERENCES Izdaja(idIzdaja),
    FOREIGN KEY(idZanr) REFERENCES Zanr(idZanr)
)

CREATE TABLE Track(
    idTrack INTEGER PRIMARY KEY AUTOINCREMENT,
    naslov TEXT NOT NULL,
    dolzina time NOT NULL,
    idizdaja INTEGER NOT NULL,
    FOREIGN KEY (idIzdaja) REFERENCES Izdaja(idIzdaja)
)

CREATE TABLE Je_Clan(
    idOseba INTEGER NOT NULL,
    idArtist INTEGER NOT NULL,
    FOREIGN KEY(idOseba) REFERENCES Oseba(idOseba),
    FOREIGN KEY(idArtist) REFERENCES Artist(idArtist)
)

CREATE TABLE Je_Sodeloval(
    idOseba INTEGER NOT NULL,
    idIzdaja INTEGER NOT NULL,
    vloga TEXT,
    FOREIGN KEY(idOseba) REFERENCES Oseba(idOseba),
    FOREIGN KEY(idIzdaja) REFERENCES Izdaja(idIzdaja)
)

CREATE TABLE Je_Avtor (
    idIzdaja INTEGER NOT NULL,
    idArtist INTEGER NOT NULL,
    FOREIGN KEY (idIzdaja) REFERENCES Izdaja (idIzdaja),
    FOREIGN KEY (idArtist) REFERENCES Artist (idArtist) 
);
