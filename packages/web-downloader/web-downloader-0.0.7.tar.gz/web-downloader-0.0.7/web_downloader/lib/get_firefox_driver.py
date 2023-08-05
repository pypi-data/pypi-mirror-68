from urllib import request
from zipfile import ZipFile
import os

def get_the_version_of_latest_firefox():
   response = request.urlopen('https://github.com/mozilla/geckodriver/releases/latest')
   redirected_url = response.geturl()
   version = redirected_url.split('/')[-1]
   return version

def main():
   # Create base firefox driver folder
   base_firefox_driver = 'firefox_driver'
   if not os.path.isdir(base_firefox_driver):
      os.mkdir(base_firefox_driver)

   latest_version = get_the_version_of_latest_firefox()
   geckodriver_file_name = f'geckodriver-{latest_version}-win64.zip'
   firefox_driver_url = f'https://github.com/mozilla/geckodriver/releases/download/{latest_version}/{geckodriver_file_name}'

   print('Downloading the latest Firefox driver from:')
   print(firefox_driver_url)

   request.urlretrieve(firefox_driver_url, geckodriver_file_name)
   with ZipFile(geckodriver_file_name, 'r') as zipObj:
      zipObj.extractall(f'firefox_driver\\{latest_version}')