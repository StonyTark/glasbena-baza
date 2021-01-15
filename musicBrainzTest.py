#Bo uporabljeno za prenos podatkov iz baze

import musicbrainzngs as mb

mb.set_useragent("MusicDB (School project)", "1.0", "/")
b = mb.search_artists("Siddharta")
print(b)

#print(mb.get_artist_by_id("22516469-fc32-4849-bdda-7d7cadf5e2b8"))
#print("----------")
#print(mb.search_areas("Slovenia"))  # id = "5b0b6225-584c-3942-b69d-5efceb9989af"

#print(mb.get_area_by_id("5b0b6225-584c-3942-b69d-5efceb9989af"))
#print([x for x in mb.search_release_groups("Siddharta")["release-group-list"] if x["artist-credit"]])


def artist_search(name, country=""):
    """
    Poišče glasbenika z imenom `name`, iz države `country`. seznam slovarjev s ključi:
        'name': (artist_name, artist_type, artist_mb_id)
        'area': (area_name, area_type, area_mb_id)
        'life-span': [date_started, date_ended]
        'genre': [list of genres preformed]
    """

    out = list()
    artists = mb.search_artists(name)["artist-list"]  # iskanje glasbenikov
    print("-----------\n", artists)

    for selected in artists:
        print(selected[""])

        # ni iz prave države
        if country and country != selected["area"]["name"]:
            continue
            
        area = selected["area"]
        l_s = selected["life-span"]
        genre = selected["tag-list"]

        data = dict()
        data["name"] = (selected["name"], selected["type"], selected["id"])
        data["area"] = (area["name"], area["type"], area["id"])
        data["life-span"] = [l_s["begin"], l_s["ended"]]
        data["genre"] = [g["name"] for g in genre]

        out.append(data)
    
    return out


print(artist_search("Siddharta", "Slovenia"))