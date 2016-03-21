import sys
import os
import shutil
from os import path
import sqlite3
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )

import unittest

from dbconfig import DBConfig

class test_db_config(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.test_dir = os.path.dirname(os.path.realpath(__file__))
        cls.test_dir = cls.test_dir + "/test_db"
        cls.db = DBConfig(cls.test_dir)

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.test_dir)

    def test_destroy_db(self):
        self.db.db_create()
        self.db.db_destroy()
        self.assertFalse(os.path.exists(self.test_dir + '/rapgenerator.db'))

    def test_create_db(self):
        self.db.db_create()
        self.assertTrue(os.path.exists(self.test_dir + '/rapgenerator.db'))

    def test_db_table_songs(self):
        self.db.db_create()
        conn=sqlite3.connect(self.test_dir+'/rapgenerator.db')
        c = conn.cursor()
        c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='songs';")
        self.assertTrue(c.fetchone()[0] == 'songs')

    def test_db_table_lyrics(self):
        self.db.db_create()
        conn=sqlite3.connect(self.test_dir+'/rapgenerator.db')
        c = conn.cursor()
        c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='lyrics';")
        self.assertTrue(c.fetchone()[0] == 'lyrics')

if __name__ == '__main__':
    unittest.main()
