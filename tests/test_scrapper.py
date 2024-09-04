import unittest
from scrapper import Scrapper

class TestScraper(unittest.TestCase):
    
    def setUp(self):
        self.scraper = Scrapper('https://news.ycombinator.com/',30,5,'less','comments', True)
        self.scraper.get_data_entries()  # Fetch data for testing
        
    def test_get_data_entries(self):
        self.assertEqual(len(self.scraper.entries), 30, "Should fetch 30 entries")
    
    def test_filter_more_than_five_words(self):
        filtered = self.scraper.filter_entries()
        for entry in filtered:
            self.assertTrue(entry['words'] <= 5, "Entry title should have less than five words")
            
    def test_order(self):
        filtered = self.scraper.filter_entries()
        sorted = self.scraper.order_entries(filtered)  
        self.assertGreater(sorted[0]['comments'],sorted[1]['comments'],"The first entry should have more comments than the second one." )

if __name__ == '__main__':
    unittest.main()