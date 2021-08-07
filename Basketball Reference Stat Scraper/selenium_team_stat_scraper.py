from selenium import webdriver
from time import sleep
import os
from datetime import date
import shutil


# This code is disgusting, but it works for now.
# I got tired of playing with bs4 and this is a quick and dirty workaround for that.


# Path to store is an absolute path to store the files.
# Default download location is where the files are downloaded to by default.
# Path to chromedriver is the path that the selenium chromedriver is stored.
    # chromedriver isn't installed by default with selenium
    # This isn't a tutorial, figure out how to get selenium working on your own.

path_to_store = ''
default_download_location = ''
path_to_chromedriver = ''


driver = webdriver.Chrome(executable_path=f"{path_to_chromedriver}")






for year in range(1980,date.today().year+1):

    try:
        os.mkdir(f'{path_to_store}/{year}/')
    except:
        pass


    driver.get(f'https://www.basketball-reference.com/leagues/NBA_{year}.html#all_team-stats-per_game')
    sleep(15)
    driver.maximize_window()


    html = driver.find_element_by_tag_name('html')

    b = driver.find_element_by_xpath('/html/body/div[2]/div[5]/div[5]/div[1]/div/ul/li[2]/span')
    print(b.location_once_scrolled_into_view)

    sleep(2)
    html.find_element_by_xpath('/html/body/div[2]/div[5]/div[5]/div[1]/div/ul/li[2]/span').click()
    sleep(.5)
    html.find_element_by_xpath('/html/body/div[2]/div[5]/div[5]/div[1]/div/ul/li[2]/div/ul/li[3]/button').click()

    sleep(2)


    b = driver.find_element_by_xpath('/html/body/div[2]/div[5]/div[8]/div[1]/div/ul/li[2]/span')
    print(b.location_once_scrolled_into_view)
    sleep(2)
    html.find_element_by_xpath('/html/body/div[2]/div[5]/div[8]/div[1]/div/ul/li[2]/span').click()
    sleep(.5)
    html.find_element_by_xpath('/html/body/div[2]/div[5]/div[8]/div[1]/div/ul/li[2]/div/ul/li[3]/button').click()




    shutil.move(f'{default_download_location}/sportsref_download.xls', f'/{path_to_store}/{year}/{year}_basic.xls')
    sleep(.5)
    shutil.move(f'{default_download_location}/sportsref_download (1).xls', f'{path_to_store}/{year}/{year}_adv.xls')
    sleep(.5)

    print(f'Done with {year}')
