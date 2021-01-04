#Bo uporabljeno za prenos podatkov iz baze

import musicbrainzngs as mb

mb.set_useragent("MusicDB (School project)", "1.0", "/")
b = mb.search_artists("Siddharta")
print(b)

print(mb.get_artist_by_id("22516469-fc32-4849-bdda-7d7cadf5e2b8"))