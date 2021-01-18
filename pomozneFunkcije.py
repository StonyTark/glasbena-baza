def pretvori_v_sekunde(niz):
    """
    Pretvori niz, ki predstavlja dolžino skladbe v formatu hh:mm:ss v število sekund.
    """
    h, m, s = map(int, niz.split(":"))
    return s + m*60 + h*3600


def sekunde_v_format(sek):
    """
    Pretvori sekunde `sek` v format hh:mm:ss.
    """
    if isinstance(sek, str):
        return sek
    h = sek // 3600
    m = (sek % 3600) // 60
    s = sek % 60
    return "{:0>2d}:{:0>2d}:{:0>2d}".format(h, m, s)

def popravi_datum(niz):
    """
    Format yyyy-mm-dd spremeni v dd. mm. yyyy.
    """
    return "{2}. {1}. {0}".format(*niz.split("-"))


if __name__ == "__main__":
    print(sekunde_v_format(11432))
    print(popravi_datum("1975-12-13"))
