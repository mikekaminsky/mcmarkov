import psycopg2
import pickle

conn_string = "host='localhost' dbname='rhymes' user='michaelkaminsky'"
conn = psycopg2.connect(conn_string)
cur = conn.cursor()

def getlyrics(artist):
    SQL = "SELECT lyrics from lyrics join songs on lyrics.song_id = songs.id where artist = %s;" # Note: no quotes
    data = (artist, )
    cur.execute(SQL, data)
    lyrics = cur.fetchall()
    return [str(i[0]).lower().split() for i in lyrics]
    #return lyrics

corpus = getlyrics('eminem')
pickle.dump(corpus, open( "eminemcorpus.pickle", "wb" ) )

