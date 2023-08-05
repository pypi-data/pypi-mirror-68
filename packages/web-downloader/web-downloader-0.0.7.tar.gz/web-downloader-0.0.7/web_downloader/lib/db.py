import os
import sqlite3
from datetime import datetime
from . import paths_management as paths

class Database:
    def __init__(self, db_path=None):
        if db_path is None:
            app_paths = paths.App_Paths()
            db_path = os.path.join(app_paths.base_script_path, 'web_downloader.db')
        self.db_path = db_path

    def check_if_db_exists(self):
        return os.path.exists(os.path.join(os.path.dirname(os.path.abspath(__file__)), self.db_path))

    def create_db(self):
        if not self.check_if_db_exists():
            with sqlite3.connect(self.db_path) as conn:
                c = conn.cursor()
                c.execute('CREATE TABLE urls (url_id integer primary key autoincrement, url text, title text, depth_level integer, file_path text, ts text)')
                c.execute('CREATE TABLE urls_from_parsing (url_from_parsing_id integer primary key autoincrement, url_id integer, url text, external_to_domain integer, title text, depth_level integer, ts text)')
                conn.commit()

    # return url_id
    def insert_url(self, url, title, depth_level, file_path):
        if self.check_if_db_exists():
            with sqlite3.connect(self.db_path) as conn:
                c = conn.cursor()
                c.execute("INSERT INTO urls (url, title, depth_level, file_path, ts) VALUES (?, ?, ?, ?, ?)", (url, title, depth_level, file_path, str(datetime.now())) )
                conn.commit()
                cursor = c.execute("SELECT last_insert_rowid() FROM urls")
                (url_id,) = cursor.fetchone()
                cursor.close()
            return url_id
        else:
            return -1

    def get_url(self, url_id):
        if self.check_if_db_exists():
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                c = conn.cursor()
                cursor = c.execute( "SELECT * FROM urls WHERE url_id = ?", (url_id,) )
                url_row = cursor.fetchone()
                cursor.close()
            return url_row
        else:
            return -1

    # To-do: return affected rows
    def update_url(self, url_id, url, title, depth_level, file_path):
        if self.check_if_db_exists():
            with sqlite3.connect(self.db_path) as conn:
                c = conn.cursor()
                c.execute("UPDATE urls SET url=?, title=?, depth_level=?, file_path=? WHERE url_id=?", (url, title, depth_level, file_path, url_id) )
                conn.commit()
    
    # return urls_from_parsing_id
    def insert_url_from_parsing(self, url_id, url, external_to_domain, title, depth_level):
        if self.check_if_db_exists():
            with sqlite3.connect(self.db_path) as conn:
                c = conn.cursor()
                c.execute("INSERT INTO urls_from_parsing (url_id, url, external_to_domain, title, depth_level, ts) VALUES (?, ?, ?, ?, ?, ?)", (url_id, url, external_to_domain, title, depth_level, str(datetime.now())) )
                conn.commit()
                cursor = c.execute("SELECT last_insert_rowid() FROM urls_from_parsing")
                (urls_from_parsing_id,) = cursor.fetchone()
                cursor.close()
            return urls_from_parsing_id
        else:
            return -1

    def get_url_from_parsing(self, url_from_parsing_id):
        if self.check_if_db_exists():
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                c = conn.cursor()
                cursor = c.execute( "SELECT * FROM urls_from_parsing WHERE url_from_parsing_id = ?", (url_from_parsing_id,) )
                url_tuple = cursor.fetchone()
                cursor.close()
            return url_tuple
        else:
            return -1

    # To-do: return affected rows
    def update_url_from_parsing(self, url_from_parsing_id, url_id, url, external_to_domain, title, depth_level):
        if self.check_if_db_exists():
            with sqlite3.connect(self.db_path) as conn:
                c = conn.cursor()
                c.execute("UPDATE urls_from_parsing SET url_id=?, url=?, external_to_domain=?, title=?, depth_level=? WHERE url_from_parsing_id=?", (url_id, url, title, external_to_domain, depth_level, url_from_parsing_id) )
                conn.commit()