from .lib import download_webpage as dl
from .lib import parse_webpage as parser
from . import create_db

def process_url(url):
    create_db.create_db()    
    url_id = dl.download_url(url, 0)
    parser.parse_url(url_id, 0)