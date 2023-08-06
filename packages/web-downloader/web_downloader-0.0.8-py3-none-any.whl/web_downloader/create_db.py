import os
from .lib import paths_management as paths
from .lib import db

def create_db():
    app_paths = paths.App_Paths()
    db_path = os.path.join(app_paths.base_script_path, 'web_downloader.db')

    if os.path.isfile(db_path) == False:
        curr_db = db.Database(db_path)
        curr_db.create_db()