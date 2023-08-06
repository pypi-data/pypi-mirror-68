import os
# import db
from . import db
from . import paths_management as paths
from selenium import webdriver

def get_domain(url):
    return url.replace('http://', '').replace('https://', '').replace('file://', '').split('/')[0]

def is_url_external(subject_url, url_for_checking):
    return get_domain(subject_url) != get_domain(url_for_checking)

def parse_url(url_id, depth_level):
    app_paths = paths.App_Paths()
    curr_db = db.Database()
    url_obj = curr_db.get_url(url_id)
    local_url = url_obj['file_path']

    assert app_paths.firefox_driver_path is not None

    with webdriver.Firefox(executable_path=app_paths.firefox_driver_path) as driver:
        driver.get(f'file://{local_url}')
        elems = driver.find_elements_by_tag_name('a')

        parsed_url_saved_counter = 0

        for elem in elems:
            href = elem.get_attribute('href')
            if href is not None:
                is_url_ext = 1 if is_url_external(url_obj['url'], href) else 0
                curr_db.insert_url_from_parsing(url_id, href, is_url_ext, elem.get_attribute('innerText'), depth_level)
                parsed_url_saved_counter += 1


    print(f'Number of parsed urls: {parsed_url_saved_counter}')