import sqlite3
import unittest
from scrapper import Scrapper

class TestScraper(unittest.TestCase):
    
    def setUp(self):
        self.scraper = Scrapper('https://news.ycombinator.com/',30,5,'less','comments', True)
        self.scraper.get_data_entries()  # Fetch data for testing
        
    def test_get_data_entries(self):
        self.assertEqual(len(self.scraper.entries), self.scraper.max_entries, "Should fetch N entries")
    
    def test_filter_more_than_five_words(self):
        filtered = self.scraper.filter_entries()
        for entry in filtered:
            self.assertTrue(entry['words'] <= self.scraper.reference_number, "Entry title should have less than N words")
            
    def test_order(self):
        filtered = self.scraper.filter_entries()
        sorted = self.scraper.order_entries(filtered)  
        self.assertGreater(sorted[0]['comments'],sorted[1]['comments'],"The first entry should have more comments than the second one." )
        
    def test_store_usage_data(self):
        conn = sqlite3.connect('database/usage_data.db')
        c = conn.cursor()
        c.execute("SELECT COUNT(*) FROM usage_data")
        count = c.fetchone()[0]
        self.scraper.run() #Execute program
        c.execute("SELECT COUNT(*) FROM usage_data")
        count2 = c.fetchone()[0]
        conn.close()
        self.assertGreater(count2,count,"The system should insert a new row" )

if __name__ == '__main__':
    unittest.main()