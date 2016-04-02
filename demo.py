from mc.mc import MCMarkov
import sqlite3
from scraper.scraper import Scraper
from scraper.dbconfig import DBConfig


# Run these lines if you are just getting started
#d = DBConfig()
#d.db_destroy()
#d.db_create()
#s = Scraper()
#s.add_songs(['gucci mane'])
#s.add_lyrics()

def getlyrics(cursor, artist):
    SQL = "SELECT line from lyrics join songs on lyrics.song_id = songs.id where artist =?;" # Note: no quotes
    data = (artist, )
    cursor.execute(SQL, data)
    lyrics = cursor.fetchall()
    return [i[0].encode('UTF-8').decode('UTF-8').lower().split() for i in lyrics]

conn=sqlite3.connect("/usr/local/sqlite/rapgenerator.db")
c = conn.cursor()
corpus = getlyrics(c, 'gucci mane')

mc = MCMarkov(corpus, 4, True)
new_song = mc.create_song(couplet_count=10, syllable_count=10)

for couplet in new_song:
    for line in couplet:
        print ' '.join(line)



for line in corpus:
    if line and '?' in line[0]:
        print line


starting_words = [line[0] for line in self.corpus if line]

