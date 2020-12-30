#Bo uporabljeno za prenos podatkov iz baze

import musicbrainzngs

musicbrainzngs.set_useragent("MusicDB (School project)", "1.0", "/")
b=musicbrainzngs.search_artists("Siddharta")
print(b)

