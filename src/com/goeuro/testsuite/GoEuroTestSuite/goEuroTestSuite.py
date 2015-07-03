'''
Author: Saritha Rajagopal
Created:30-June-2015
Description:Checks the sorting of travel cost between two locations
'''  

import unittest
import time
import logging
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException

'''
    Global variables are created for source and destination locations.
'''

BERLIN = 'Berlin, Germany'
PRAGUE = 'Prague, Czech Republic'

class goEuroTestSuite(unittest.TestCase):
    
    '''
    Navigates to the page given in the URL.
    ''' 
    def setUp(self):    
        self.driver=webdriver.Chrome()
        self.driver.get("http://www.goeuro.com/")
        self.driver.maximize_window()
        
    '''
    Accepts and enters the source and destination locations into the text box. 
    Input Arguments:Source location,destination location
    '''      
    def source_dest_entry(self,src,dest):
        driver=self.driver
        source=driver.find_element_by_id('from_filter')    
        source.send_keys(src)
        destination=driver.find_element_by_id('to_filter')
        destination.send_keys(dest)
        destination.send_keys(Keys.ENTER)        
                 
    '''
    Checks the title of the page.
    '''         
    def test_page_title(self):
        driver=self.driver
        driver.implicitly_wait(4)
        expected_title = 'Search & Compare Cheap Buses, Trains & Flights | GoEuro'
        assert expected_title in driver.title
        
    '''
    Enters the same location as source and destination into the text box.
    '''  
    def test_main_page_search_negative(self):
        driver=self.driver
        self.source_dest_entry(BERLIN,BERLIN)
        message="//div[@class='five columns to-box']/ul[1]/li"
        expected_alert_msg='Please enter two different locations.'
        WebDriverWait(driver,10).until(EC.text_to_be_present_in_element((By.XPATH,message), expected_alert_msg))
    
    '''
    Checks the search functionality by entering different source and destination locations. 
    '''      
    def test_main_page_search_positive(self):
        driver=self.driver
        time.sleep(5)             
        self.source_dest_entry(BERLIN,PRAGUE)
        search_button = driver.find_element_by_id('search-form__submit-btn')
        driver.implicitly_wait(8)    
        search_button.click()
        try:
            WebDriverWait(driver,8).until(EC.text_to_be_present_in_element_value((By.ID,'from_filter'),BERLIN))
            WebDriverWait(driver,8).until(EC.text_to_be_present_in_element_value((By.ID,'to_filter'),PRAGUE))
        except TimeoutException:
            assert False,"Timeout exception raised" 
        driver.implicitly_wait(10)  

    '''
       Checks if the prices of all the travel modes are sorted.
    '''    
    def test_sort_price(self):
        logging.basicConfig(level=logging.INFO)
        driver=self.driver
        self.test_main_page_search_positive()
        driver.find_element_by_link_text('Cheapest').click()
        train="//a[@class='ico-train-2 no-outline']"
        flight="//a[@class='ico-flight-2 no-outline']"
        bus="//a[@class='ico-bus-2 no-outline']"
        closebuttton="//a[@class='close']"
        xtrain=driver.find_element_by_xpath(train)
        xflight=driver.find_element_by_xpath(flight)
        xbus=driver.find_element_by_xpath(bus)
        xclosebutton=driver.find_element_by_xpath(closebuttton)
        travelmode=[xtrain,xflight,xbus]
        for tmode in travelmode:
            tmode.click()
            amount="//div[@class='price-cell-content']/span[1]"
            if(tmode == xflight):
                time.sleep(4)
                xclosebutton.click()
                amount="//div[@class='price-cell-total']/span[1]"
            logging.info(tmode.text)
            list_price = []
            xamount=driver.find_elements_by_xpath(amount)
            time.sleep(5)
            for travel_cost in xamount:                   
                price_text = travel_cost.text[1:]
                if price_text != '':
                    list_price.append(float(price_text))
                    logging.info(price_text)            
            logging.info(list_price)            
            if len(list_price) > 0:
                sorting = all(list_price[i] <= list_price[i+1] for i in range(len(list_price)-1))
                assert bool(sorting) == True,'Prices not in sorted order'              
     

    '''
       Exits the entire browser.
    '''           
    def tearDown(self):
        self.driver.quit()  
     
if __name__=='__main__':
    unittest.main()
        
        
