import os
import shutil
from .lib import paths_management as paths

app_paths = paths.App_Paths()
db_path = os.path.join(app_paths.base_script_path, 'web_downloader.db')

if os.path.isfile(db_path):
    os.remove(db_path)
if os.path.isdir('web_data'):
    shutil.rmtree('web_data')
if os.path.isdir('firefox_driver'):
    shutil.rmtree('firefox_driver')