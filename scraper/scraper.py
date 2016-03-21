import sqlite3
import os.path
import re
from pygenius import songs as pygenius_songs

class Scraper(object):
    """
    Class to serve as a container for updating the rapgenerator database
    """
    def __init__(self, db_loc = None, additional_skip_terms = []):

        self.bad_terms = [
               ' by ',
               'album art',
               'credits',
               'interview',
               'skit',
               'dates',
               'interview'
                ] + additional_skip_terms


        print "Scraper object created"
        if db_loc is None:
            self.db_loc = "/usr/local/sqlite"
        else:
            self.db_loc = db_loc

        if os.path.exists(self.db_loc + '/rapgenerator.db'):
            conn=sqlite3.connect(self.db_loc+'/rapgenerator.db')
            print("Database found")
        else:
            print("ERROR: Databse not found. Try using DBSetup()")
            raise

        self.conn = conn

    def add_songs(self, artist_list):
        """
        Method to find and add new songs to the songs table.
        """

        "Terms that identify songs that aren't really songs"
        conn = self.conn
        conn.text_factory = str
        c = conn.cursor()

        if artist_list is None:
            return "You must provide a list of artists for whom to find songs."
        else:
            for artist in artist_list:
                print("Finding songs for " + artist)
                all_songs_by_artist = pygenius_songs.findAllSongs(artist)
                already_scraped = list()
                for song in all_songs_by_artist:
                    url = song[0]
                    title = song[1]
                    print(title)
                    c.execute("SELECT count(*) FROM songs WHERE title = (?) AND artist = (?)", (title, artist))
                    check_in_db = c.fetchall()
                    if check_in_db[0][0] == 0:
                        if title not in already_scraped:
                            if not [i for i, x in enumerate(self.bad_terms) if x in title]:
                                already_scraped.append(title)
                                c.execute('INSERT INTO songs(title, artist, url) values (?,?,?)', (title, artist, url))
                    conn.commit()

    def add_lyrics(self):
        """
        Method to add lyrics for any songs that don't have them
        """

        conn = self.conn
        conn.text_factory = str
        c = conn.cursor()

        c.execute("SELECT songs.id, artist, title, url FROM songs LEFT JOIN lyrics ON songs.id = lyrics.song_id WHERE lyrics.song_id IS NULL")
        all_songs_to_scrape = c.fetchall()
        for song in all_songs_to_scrape:
            song_id = song[0]
            song_artist = song[1]
            song_title = song[2]
            song_url = song[3]
            print("Looking for lyrics for " + song_title + " by " + song_artist)
            try:
                lyrics = pygenius_songs.searchURL(song_url, 'lyrics')
                for lyric in lyrics:
                    for line in lyric.split('\n'):
                        c.execute('INSERT INTO lyrics(song_id, line) VALUES (?,?)', (song_id, line))
                        conn.commit()
            except Exception as e:
                print(e)
                print song_url
                print("Exception caught! ... continuing.")
                pass
