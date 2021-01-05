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
    #TODO
    bottle.redirect("/")

@bottle.get("/iskanje")
def iskanje():
    iskaniNiz=bottle.request.query.get('iskaniNiz','')
    izbira=bottle.request.query.get('izbira','1')
    if izbira=='1':
        return bottle.template('iskanje.html', niz=iskaniNiz, izbira=izbira, podatki=model.Artist.poisci(iskaniNiz))
    elif izbira=='2':
        return bottle.template('iskanje.html', niz=iskaniNiz, izbira=izbira, podatki=model.Oseba.poisci(iskaniNiz))
    elif izbira=='3':
        return bottle.template('iskanje.html', niz=iskaniNiz, izbira=izbira, podatki=model.Izdaja.poisci(iskaniNiz))
    

bottle.run(debug=True, reloader=True)

