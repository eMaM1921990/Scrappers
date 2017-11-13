from telnetlib import EC

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

__author__ = 'eMaM'
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class Robots():

    def Test(self):
        driver = webdriver.Chrome('/Users/mac/Downloads/chromedriver')
        # driver.maximize_window()
        driver.get("https://sfbay.craigslist.org/fb/sfo/vac/6331031900")
        mainWin = driver.current_window_handle
        driver.execute_script("$('#recaptcha-anchor').click()")
        print driver.page_source
        # move the driver to the first iFrame
        # iframe = driver.switch_to_frame(driver.find_elements_by _tag_name("iframe"))
        # print iframe
        # iframe.click()





        # driver.find_element_by_id('standalone_captcha')
        # el = driver.switch_to_frame(driver.find_element_by_tag_name('iframe'))
        # driver.find_element_by_id("recaptcha-anchor").click()
        # search_box = driver.s(driver.find_element_by_id("recaptcha-anchor"))
        # search_box = driver.find_element_by_id("recaptcha-anchor")
        # result = search_box.click()
        # print el.tag_name
        # driver.quit()


Robots().Test()