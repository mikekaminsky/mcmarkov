import sqlite3
import os.path

class DBConfig(object):
    """
    Class to serve as a container for setting up the db for the rap generator
    """
    def __init__(self, db_loc = None):

        print "DBSetup object created"
        if db_loc is None:
            self.db_loc = "/usr/local/sqlite"
        else:
            self.db_loc = db_loc
        print("DB at " + self.db_loc + " will be modified.")

    def db_destroy(self):
        """
        Method to destroy existing sqlite database
        """

        db_loc = self.db_loc

        if os.path.exists(db_loc + '/rapgenerator.db'):
            os.remove(db_loc + '/rapgenerator.db')
            print "Database " + db_loc + '/rapgenerator.db' + " successfully destroyed"
            return True
        else:
            print "No rapgenerator.db database at "+ db_loc
            return False

    def db_create(self):
        """
        Method to create a new database.
        Check to see if the db exists already. If not, create it.
        """

        db_loc = self.db_loc

        if not os.path.exists(db_loc):
            os.makedirs(db_loc)
        if not os.path.exists(db_loc+'/rapgenerator.db'):
            conn=sqlite3.connect(db_loc+'/rapgenerator.db')
            print "Database created and opened succesfully at " + db_loc + 'rapgenerator.db'
        else:
            print "ERROR: A rapgenerator db already exists at " + db_loc

        conn.text_factory = str
        c = conn.cursor()
        c.execute(' DROP TABLE IF EXISTS songs; ')
        c.execute(' CREATE TABLE songs (id integer primary key, title text, artist text, url text); ')
        c.execute(' DROP TABLE IF EXISTS lyrics; ')
        c.execute(' CREATE TABLE lyrics (id integer primary key, song_id integer, line text); ')
        conn.close()
