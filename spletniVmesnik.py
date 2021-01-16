import bottle
import model

@bottle.get("/")
def zacetna_stran():
    return bottle.template('zacetna.html')

@bottle.get("/dodaj")
def dodaj():
    return bottle.template('dodaj.html')

@bottle.post("/dodaj")
def dodaj_post():
    
    izbira=bottle.request.forms.getunicode("izbira")
    if izbira=='1':
        ime = bottle.request.forms.getunicode("vnos1")
        priimek = bottle.request.forms.getunicode("vnos2")
        datumRojstva = bottle.request.forms.getunicode("vnos3")
        spol = bottle.request.forms.getunicode("vnos4")
        drzava = bottle.request.forms.getunicode("vnos5")
        oseba = model.Oseba(ime,priimek,datumRojstva,spol,drzava)
        oseba.dodaj_v_bazo()

        return bottle.template("oseba.html", iskanId=oseba.id, podatki=oseba)
    
    elif izbira=='2':
        koliko = int(bottle.request.forms.getunicode("koliko"))
        ime = bottle.request.forms.getunicode("vnos1")
        leto = bottle.request.forms.getunicode("vnos2")
        drzava = bottle.request.forms.getunicode("vnos3")
        mesto = bottle.request.forms.getunicode("vnos4")

        clani=[]
        for i in range(5,koliko+1):
            temp=bottle.request.forms.getunicode("vnos{}".format(i))
            clani.append(int(temp))
        
        art=model.Artist(ime,leto,drzava,mesto)
        art.dodaj_v_bazo()
        art.dodaj_clane(clani)

        return bottle.template("artist.html", iskanId=art.id, podatki=art)

    
    elif izbira=='3':
        koliko = int(bottle.request.forms.getunicode("koliko"))
        naslov = bottle.request.forms.getunicode("vnos1")
        leto = bottle.request.forms.getunicode("vnos2")
        celotnaDolzina = bottle.request.forms.getunicode("vnos3")
        tip = bottle.request.forms.getunicode("vnos4")
        idZalozbe = bottle.request.forms.getunicode("vnos5")
        if idZalozbe=='':
            idZalozbe=None
        else:
            idZalozbe=int(idZalozbe)

        avtorji=[]
        for i in range(6,koliko+1):
            temp=bottle.request.forms.getunicode("vnos{}".format(i))
            avtorji.append(int(temp))

        izd=model.Izdaja(naslov,leto,tip,celotnaDolzina,idZalozbe)
        izd.dodaj_v_bazo()
        izd.dodaj_avtorje(avtorji)

        return bottle.template("izdaja.html", iskaniID=izd.id , podatki=izd)
    

@bottle.get("/iskanje")
def iskanje():
    iskaniNiz=bottle.request.query.get('iskaniNiz','')
    izbira=bottle.request.query.get('izbira','1')
    if izbira=='1':
        return bottle.template('iskanje.html', niz=iskaniNiz, izbira=izbira, podatki=model.Artist.poisci(iskaniNiz))
    elif izbira=='2':
        priimek=bottle.request.query.get('iskaniNizAlt','')
        return bottle.template('iskanje.html', niz=iskaniNiz, izbira=izbira, podatki=model.Oseba.poisci(ime=iskaniNiz,priimek=priimek))
    elif izbira=='3':
        return bottle.template('iskanje.html', niz=iskaniNiz, izbira=izbira, podatki=model.Izdaja.poisci(iskaniNiz))


@bottle.get("/oseba/<id>")
def oseba(id):
    return bottle.template('oseba.html', iskaniID=id , podatki=model.Oseba.poisciID(id))


@bottle.get("/artist/<id>")
def artist(id):
    return bottle.template('artist.html', iskaniID=id , podatki=model.Artist.poisciID(id))

@bottle.post("/artist/<id>")
def artist_post(id):
    id_oseba = bottle.request.forms.getunicode("id")
    model.Artist.poisciID(id).dodaj_clane([id_oseba,])
    return bottle.template("artist.html", iskanID=id, podatki=model.Artist.poisciID(id))

@bottle.get("/izdaja/<id>")
def izdaja(id):
    return bottle.template('izdaja.html', iskaniID=id , podatki=model.Izdaja.poisciID(id))
    

bottle.run(debug=True, reloader=True)

