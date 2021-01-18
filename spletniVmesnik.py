import bottle
import model
import pomozneFunkcije as pf

@bottle.get("/")
def zacetna_stran():
    
    return bottle.template('zacetna.html', zanr=model.Zanr(None), artist=model.Artist.dummy(), izdaje=model.Izdaja.dummy())

@bottle.post("/")
def zacetna_stran_post():
    print("=====================")
    vnosi=[]
    for i in range(model.Zanr.prestej_zvrsti()):
        vnosi.append(bottle.request.forms.getunicode("izbiraZvrst"+str(i)))
    print(vnosi)
    
    izbrane_drzave=set(bottle.request.forms.getunicode("drzave").split(',')[:-1]) #(odbijem vejico)
    print(izbrane_drzave)

    izbrani_ust=set(bottle.request.forms.getunicode("ustvarjalci").split(',')[:-1])
    print(izbrani_ust)
    bottle.redirect("/")

@bottle.get("/dodaj")
def dodaj():
    return bottle.template('dodaj.html',osebe=model.Oseba.dummy(),artisti=model.Artist.dummy(), zalozbe=model.Zalozba.dummy()) #dummy objekt da lahko kličemo metode v html strani brez importa

@bottle.post("/dodaj")
def dodaj_post():
    
    izbira=bottle.request.forms.getunicode("izbira")
    if izbira=='1':
        ime = bottle.request.forms.getunicode("vnos1")
        priimek = bottle.request.forms.getunicode("vnos2")
        datumRojstva = bottle.request.forms.getunicode("vnos3")
        spol = bottle.request.forms.getunicode("idS")
        drzava = bottle.request.forms.getunicode("vnos5")
        oseba = model.Oseba(ime,priimek,datumRojstva,spol,drzava)
        oseba.dodaj_v_bazo()
        bottle.redirect("/oseba/"+str(oseba.id))
    
    elif izbira=='2':
        
        ime = bottle.request.forms.getunicode("vnos1")
        leto = bottle.request.forms.getunicode("vnos2")
        drzava = bottle.request.forms.getunicode("vnos3")
        mesto = bottle.request.forms.getunicode("vnos4")

        art=model.Artist(ime,leto,drzava,mesto)
        art.dodaj_v_bazo()

        koliko=bottle.request.forms.getunicode("koliko")
        if koliko != '':
            koliko = int(koliko)
            clani=[]
            for i in range(5,koliko+1):
                temp=bottle.request.forms.getunicode("vnos{}".format(i))
                clani.append(int(temp))
            art.dodaj_clane(clani)
        bottle.redirect("/artist/"+str(art.id))
            
    elif izbira=='3':
        
        naslov = bottle.request.forms.getunicode("vnos1")
        leto = bottle.request.forms.getunicode("vnos2")
        celotnaDolzina = 0
        tip = bottle.request.forms.getunicode("vnos4")
        idZalozbe = bottle.request.forms.getunicode("id")
        if idZalozbe=='':
            idZalozbe=None
        else:
            idZalozbe=int(idZalozbe)

        izd=model.Izdaja(naslov,leto,tip,celotnaDolzina,idZalozbe)
        izd.dodaj_v_bazo()

        koliko = bottle.request.forms.getunicode("koliko")
        avtorji=[]
        if koliko!='':
            koliko=int(koliko)
            for i in range(6,koliko+1):
                temp=bottle.request.forms.getunicode("vnos{}".format(i))
                avtorji.append(int(temp))
            izd.dodaj_avtorje(avtorji)   
        bottle.redirect("/izdaja/"+str(izd.id))
        
    elif izbira == '4':
        
        zanr=bottle.request.forms.getunicode('vnos1', '')
        model.Zanr(zanr).dodaj_v_bazo()
        bottle.redirect("/dodaj")
    
    elif izbira == '5':

        ime=bottle.request.forms.getunicode('vnos1', '')
        drzava=bottle.request.forms.getunicode('vnos2', '')
        model.Zalozba(ime, drzava).dodaj_v_bazo()
        bottle.redirect("/dodaj")

@bottle.get("/iskanje")
def iskanje():
    izbira=bottle.request.query.get('izbira', '')
    data=[None,None,None]
    if izbira=='1':
        ime=bottle.request.query.get('vnos1','')
        leto1=bottle.request.query.get('vnos2',1900)
        leto2=bottle.request.query.get('vnos3',2030)
        drzava=bottle.request.query.get('vnos4','')
        mesto=bottle.request.query.get('vnos5','')
        if leto1=='':
            leto1=1900
        if leto2=='':
            leto2=2030
        data=[
            model.Artist.poisci_po_vsem(ime,leto1,leto2,drzava,mesto),
            None,
            None
        ]
        
    
    elif izbira=='2':
        ime=bottle.request.query.get('vnos1','')
        priimek=bottle.request.query.get('vnos2','')
        dat_od=bottle.request.query.get('vnos3','1900-01-01')
        dat_do=bottle.request.query.get('vnos4','2030-01-01')
        spol=bottle.request.query.get('vnos5','')
        drzava=bottle.request.query.get('vnos6','')
        print("----", dat_od, dat_do, isinstance(dat_od, str))
        if dat_od=='':
            dat_od='1900-01-01'
        if dat_do=='':
            dat_do='2030-01-01'
        data=[
            None,
            model.Oseba.poisci_po_vsem(ime,priimek,dat_od,dat_do,spol,drzava),
            None
        ]
    
    elif izbira=='3':
        naslov=bottle.request.query.get('vnos1','')
        leto1=bottle.request.query.get('vnos2',1900)
        leto2=bottle.request.query.get('vnos3',2030)
        tip=bottle.request.query.get('vnos4','')
        if leto1=='':
            leto1=1900
        if leto2=='':
            leto2=2030
        data=[
            None,
            None,
            model.Izdaja.poisci_po_vsem(naslov,leto1,leto2,tip)
        ]
        print(data[2])

    return bottle.template('iskanje.html', izbira=izbira, podatki=data)

@bottle.get("/oseba/<id>")
def oseba(id):
    podatki = model.Oseba.poisciID(id)
    rojstvo = pf.popravi_datum(podatki.datumRojstva)
    return bottle.template('oseba.html', iskaniID=id , podatki=podatki, rojstvo=rojstvo)

@bottle.post("/oseba/<id>")
def oseba_post(id):
    gumb=bottle.request.forms.getunicode("submit")
    if gumb=="brisi":
        model.Oseba.brisiID(id)
    bottle.redirect("/")


@bottle.get("/artist/<id>")
def artist(id):
    return bottle.template('artist.html', iskaniID=id , podatki=model.Artist.poisciID(id))

@bottle.post("/artist/<id>")
def artist_post(id):
    gumb = bottle.request.forms.getunicode("gumb")
    if gumb == "Submit":
        artistId = bottle.request.forms.getunicode("id")
        model.Artist.poisciID(id).dodaj_clane([artistId,]) # treba dodelat funkcijo, trenutno crashne, če dodaš osebo, ki je že član
        return bottle.template('artist.html', iskaniID=id , podatki=model.Artist.poisciID(id)) 
    elif gumb == "briši":
        model.Artist.brisiID(id)
        bottle.redirect("/")
    else:
        model.Artist.dummy().brisiClana(id, gumb)
        return bottle.template('artist.html', iskaniID=id , podatki=model.Artist.poisciID(id)) 

@bottle.get("/izdaja/<id>")
def izdaja(id):
    podatki = model.Izdaja.poisciID(id)
    podatki.nastavi_dolzino(id)
    zalozba = model.Zalozba.dummy().vrni_zalozbo(podatki.idZalozbe)
    print(zalozba)
    return bottle.template('izdaja.html', iskaniID=id , podatki=podatki, artisti=model.Artist.dummy(), zalozba=zalozba)

@bottle.post("/izdaja/<id>")
def izdaja_post(id):
    gumb=bottle.request.forms.getunicode("gumb")
    print("WE HERE")
    if gumb=='Dodaj skladbo':
        naslov = bottle.request.forms.getunicode("naslov")
        dolzina = bottle.request.forms.getunicode("dolzina")
        model.Track(naslov, pf.pretvori_v_sekunde(dolzina), id).dodaj_v_bazo()
        model.Izdaja.nastavi_dolzino(id)
        podatki = model.Izdaja.poisciID(id)
        zalozba = model.Zalozba.dummy().vrni_zalozbo(podatki.idZalozbe)
        return bottle.template("izdaja.html", iskaniID=id , podatki=podatki, artisti=model.Artist.dummy(), zalozba=zalozba)
    elif gumb=='Dodaj zvrst':
        izbraniZanr = bottle.request.forms.getunicode("izbraniZanr")
        model.Izdaja.poisciID(id).dodaj_zanr(int(izbraniZanr))
        podatki = model.Izdaja.poisciID(id)
        zalozba = model.Zalozba.dummy().vrni_zalozbo(podatki.idZalozbe)
        return bottle.template("izdaja.html", iskaniID=id , podatki=podatki, artisti=model.Artist.dummy(), zalozba=zalozba)
    elif gumb == "Dodaj avtorja":
        izbran = bottle.request.forms.getunicode("izbraniArtist")
        model.Izdaja.poisciID(id).dodaj_avtorje([izbran])
        bottle.redirect("/izdaja/"+str(id))
        #return bottle.template("izdaja.html", iskaniID=id , podatki=model.Izdaja.poisciID(id), artisti=model.Artist.dummy())
    elif gumb=='briši':
        model.Izdaja.brisiID(id)
        bottle.redirect("/")
    else:
        brisanID=bottle.request.forms.getunicode("brisanID")
        model.Track.izbrisi_ID(int(brisanID))
        model.Izdaja.nastavi_dolzino(id)
        bottle.redirect("/izdaja/"+str(id))

    
bottle.run(debug=True, reloader=True)

