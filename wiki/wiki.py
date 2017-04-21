#!/usr/bin/python
# -*- coding: utf-8 -*-

""" 
@author d0evi1
@date   2016.1.23
"""  
  
import time
import re
import os
import sys
import codecs
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import selenium.webdriver.support.ui as ui
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchWindowException
from selenium.common.exceptions import TimeoutException
import shutil
import traceback  

URL_PREFIX="https://zh.wikipedia.org/wiki/"

#---------------------------
#
#---------------------------
def createDriver():

    # use no-picture model. 
    chromeOptions = webdriver.ChromeOptions()
    prefs = {"profile.managed_default_content_settings.images":2}
    chromeOptions.add_experimental_option("prefs",prefs)
    
    driver = webdriver.Chrome(chrome_options=chromeOptions)

    # hidden window.
    driver.set_window_position(-2000,0)
    return driver

def createDriver2():
    return webdriver.Chrome()
    pass
	

driver = createDriver() 
wait = ui.WebDriverWait(driver,10)


file_num = 1

#-------------------------
#Get the infobox  
#------------------------
def getInfobox(name, fileName):
    global file_num
    global driver
    global wait
    try:  
        print name.rstrip('\n')
        driver.get(URL_PREFIX + name)
        #print driver.current_url

        #爬取文本信息 共10段信息
        elem_value = driver.find_elements_by_xpath("//div[@id='mw-content-text']/p")
        if len(elem_value) == 0:
            return

        file_num = file_num + 1
        print u'文件名称: ', fileName
        info = codecs.open(fileName, 'w', 'utf-8')
        info.write(name.rstrip('\n')+'\r\n')  #codecs不支持'\n'换行

        num = 0
        for value in elem_value:
            print value.text.encode('GB18030')
            info.writelines(value.text + '\r\n')
            if num >= 100:
                break
            num+=1

        time.sleep(0.5)
    except NoSuchWindowException,e:
        print "Error: ",e
        print traceback.print_exc()
        #print '\n'
        if 'info' in dir():
            info.close()
        #driver.close()	
        driver = createDriver() 
        wait = ui.WebDriverWait(driver,10)
    except TimeoutException, e:
        print "Error: ",e
        print traceback.print_exc()

        #driver.close()	
        #driver = createDriver() 
        #wait = ui.WebDriverWait(driver,10)
    except Exception,e:  #'utf8' codec can't decode byte  
        print "Error: ",e
        print traceback.print_exc()
    finally:
        if 'info' in dir():
            info.close()

#-----------------------------
#Main function
#-----------------------------
def main():
    # save directory.
    path = "download/"
    if os.path.exists(path) == False:
        os.makedirs(path)
        print "create download dir..."

    # input file.
    global driver    
    source = open("input.txt", 'r')
    i = 0

    for entityName in source:
        entityName = unicode(entityName, "utf-8")

        # reload every 150 times.
        i = i+1
        if i >= 150:
            i = 0
            driver.close()
            driver.quit()
            driver = createDriver() 
            wait = ui.WebDriverWait(driver,10)	

        name = "%d" % file_num
        fileName = path + str(name) + ".txt"
        getInfobox(entityName, fileName)

    print 'finish crawler!'
    source.close()
    driver.close()

if __name__ == '__main__':
    main()  
