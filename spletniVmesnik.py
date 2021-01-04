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
def izpis():
    iskaniNiz = bottle.request.query.get("iskaniNiz")
    return bottle.template('iskanje.html', niz=iskaniNiz, podatki=model.Artist.poisci(iskaniNiz))

bottle.run(debug=True, reloader=True)

