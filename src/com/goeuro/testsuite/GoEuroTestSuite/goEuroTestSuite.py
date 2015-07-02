'''
Author: Saritha Rajagopal
Created:30-June-2015
Description:Checks the sorting of travel cost between two locations
'''  

import unittest

from selenium import webdriver

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
    Checks the title of the page.
    '''         
    def test_page_title(self):
        driver=self.driver
        driver.implicitly_wait(4)
        expected_title = 'Search & Compare Cheap Buses, Trains & Flights | GoEuro'
        assert expected_title in driver.title

    '''
       Exits the entire browser.
    '''           
    def tearDown(self):
        self.driver.quit()  
     
if __name__=='__main__':
    unittest.main()
        
        
