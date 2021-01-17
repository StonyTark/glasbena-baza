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


if __name__ == "__main__":
    print(sekunde_v_format(11432))