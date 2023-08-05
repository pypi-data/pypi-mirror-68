from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_element_located
import pyautogui
import time
from . import db
from . import paths_management as paths
import os

def occupy_url_table_row():
    curr_db = db.Database()
    url_id = curr_db.insert_url('', '', -2, '')
    assert url_id >= 0
    return url_id

def insert_url_to_db(url_id, url, title, depth_level, file_path):
    curr_db = db.Database()
    curr_db.update_url(url_id, url, title, depth_level, file_path)

def download_url(url, curr_depth_level, wait_time=5, retry=2):
    app_paths = paths.App_Paths()

    # Create directory if the firefox driver directory is not created
    if not os.path.exists(app_paths.base_firefox_driver_path):
        os.mkdir(app_paths.base_firefox_driver_path)

    # Execute the script to download Firefox driver
    from . import get_firefox_driver as webdriver_getter
    if len(os.listdir(app_paths.base_firefox_driver_path)) == 0:
        webdriver_getter.main()

    assert app_paths.try_set_firefox_driver_path() is not None
    
    print('Using Firefox driver from:')
    print(app_paths.firefox_driver_path)

    # Create web data directory
    if not os.path.isdir(app_paths.base_web_data_dir_path):
        os.mkdir(app_paths.base_web_data_dir_path)

    url_id = occupy_url_table_row()

    page_title = '__blank__'
    file_path = os.path.join(app_paths.base_web_data_dir_path, f'{url_id}.html')

    while True:
        if os.path.isfile(file_path):
            break
        if retry == 0:
            print('Exceeded retry')
            break

        with webdriver.Firefox(executable_path=app_paths.firefox_driver_path) as driver:
            driver.get(url)
            time.sleep(wait_time)
            page_title = driver.title
            pyautogui.hotkey('ctrl', 's')
            time.sleep(1)
            
            pyautogui.typewrite(file_path)
            time.sleep(2)
            pyautogui.hotkey('enter')
            time.sleep(5)
        retry -= 1

    insert_url_to_db(url_id, url, page_title, curr_depth_level, file_path)

    return url_id