# -*- coding: utf-8 -*-
from selenium import webdriver
from models import City
import time
import requests
import os
from selenium.webdriver.support.ui import WebDriverWait
chromedriver_path = '/Users/sp41mer/PycharmProjects/parcer/chromedriver'
ghostdriver_path = '/Users/sp41mer/PycharmProjects/insta_photo_parser/phantomjs'
for city in City.select().where(City.rank>77):
    #driver_for_page = webdriver.Chrome(chromedriver_path)
    driver_for_page = webdriver.PhantomJS(ghostdriver_path)
    url = city.ig_link
    name_of_town = url.split('.com/')[1].split('/')[0]
    directory = 'photos_all/'+name_of_town
    if not os.path.exists(directory):
        print directory
        os.makedirs(directory)
        driver_for_page.get(url)
        driver_for_page.execute_script('window.scrollTo(0,document.body.scrollHeight);')
        try:
            button_more = driver_for_page.find_element_by_css_selector('a._oidfu')
        except:
            print 'Couldnt find a._oidfu'
            button_more = None
        try:
            button_more = driver_for_page.find_element_by_xpath(u"//*[contains(text(), 'Загрузить еще')]")
        except:
            print 'Couldnt find by russian text'
        try:
            button_more = driver_for_page.find_element_by_xpath(u"//*[contains(text(), 'Load more')]")
        except:
            print 'Couldnt find by english text'
        if button_more:
            button_more.click()
            for i in range(0, 10):
                driver_for_page.execute_script('window.scrollTo(0, document.body.scrollHeight / 2);')
                driver_for_page.execute_script('window.scrollTo(0,document.body.scrollHeight);')
                time.sleep(1)
            rows_of_photos = driver_for_page.find_elements_by_css_selector('div._myci9')
            number = 0
            for row in rows_of_photos:
                if number > 49:
                    break
                else:
                    photos = row.find_elements_by_css_selector('img._icyx7')
                    for photo in photos:
                        filename = 'photos_all/' + name_of_town + '/' + str(number) + '.jpg'
                        f = open(filename, 'wb')
                        f.write(requests.get(photo.get_attribute("src")).content)
                        f.close()
                        number += 1
        driver_for_page.quit()
    else:
        city.photos_path = directory
        print directory
        city.save()
        driver_for_page.close()
