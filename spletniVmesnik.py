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

@bottle.get("/izpis")
def izpis():
    bottle.template('izpis.html')

bottle.run(debug=True, reloader=True)

