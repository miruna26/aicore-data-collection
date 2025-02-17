from scraper.autotrader_scraper import Autotrader_scraper
import unittest
from bs4 import BeautifulSoup
import urllib.request
import re

from scraper.vehicle_data import Vehicle_data

class ScraperTestCase(unittest.TestCase):
    
    def setUp(self):
        self.vehicle_data_list = []
        self.test_make = "Lotus"
        self.test_model = "Exige"
    
    def test_search_vehicle_type(self):
        """
        Check that search is completed and new url is reached including search terms
        """
        self.test_scraper = Autotrader_scraper()
        init_url = self.test_scraper.driver.current_url[:-1]
        self.test_scraper.search_vehicle_type(self.test_make, self.test_model)
        new_url = self.test_scraper.driver.current_url[:-1]
        self.assertTrue(init_url != new_url and self.test_make in new_url and self.test_model in new_url)

    def test_get_vehicle_list(self):
        """
        Check that number of listed vehicles matches number of results scraped.
        """
        test_search_results_url = "https://www.autotrader.co.uk/car-search?postcode=ba229sz&make=Lotus&model=Exige&include-delivery-option=on&advertising-location=at_cars&page=1"
        self.test_scraper = Autotrader_scraper(test_search_results_url)
        
        def scrape_num_results(test_search_results_url):
            page = urllib.request.urlopen(test_search_results_url)
            soup = BeautifulSoup(page, 'html.parser')
            num_results = soup.find('h1', class_='search-form__count js-results-count').get_text()
            return int(re.sub("[^0-9]",'',num_results))
        
        self.vehicle_data_list = self.test_scraper.get_vehicle_list()
        self.assertTrue(len(self.vehicle_data_list) == scrape_num_results(test_search_results_url))

    def test_add_vehicle_page_data(self):
        """
        Check for all data added to Vehicle_data is non-empty for sample of pages.
        """
        self.vehicle_data_list = Vehicle_data.import_vehicle_data_list("test/test_files/initial_vehicle_data_list.json")
        self.test_scraper = Autotrader_scraper()
        num_samples = min([3,len(self.vehicle_data_list)])
        self.vehicle_data_list = self.test_scraper.add_vehicle_page_data(self.vehicle_data_list[:num_samples])
        for vehicle in self.vehicle_data_list:
            vehicle_data = vehicle.get_data()
            self.assertTrue(vehicle_data["id"] and vehicle_data["uuid"])
            for data in vehicle_data["data"].values():
                self.assertTrue(data)

    def tearDown(self):
        self.test_scraper.close_session()


if __name__ == "__main__":
    unittest.main(argv=[''], verbosity=2, exit=False)