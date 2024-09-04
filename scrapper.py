import requests
from bs4 import BeautifulSoup
import re

"""Definition for scrapper class
author: Gabriel Vivas
create: 04/09/2024"""

class Scraper:
    def __init__(self,url,max_entries,reference_number,word_count,order_by,order):
        self.base_url = url
        self.max_entries=max_entries
        self.reference_number=reference_number
        self.word_count=word_count
        self.order_by=order_by
        self.order=order
        self.entries = []

    def get_data_entries (self):
        response = requests.get(self.base_url)
        if response.status_code ==200:
            soup = BeautifulSoup(response.text,'html.parser')
            items = soup.select('.athing')
            for item in items[:self.max_entries]:  # Get only the first 30 entries
                number = int(item.select_one('.rank').text.strip('.'))
                title = item.select_one('.titleline > a').text
                words=self.count_words(title)
                subtext = item.find_next_sibling('tr').select_one('.subtext')
                points = int(subtext.select_one('.score').text.split()[0]) if subtext.select_one('.score') else 0 # Some entries don't have points
                comments = subtext.select('a')[-1].text
                comments = int(comments.split()[0]) if 'comment' in comments else 0 # Some entries don't have comments number
                self.entries.append({
                    'number': number,
                    'title': title,
                    'words': words,
                    'points': points,
                    'comments': comments
                })
        else:
            print(f' Request error {response.status_code}')
    
    def count_words(self,text):
        text = re.sub(r'[^\w\s]', '', text)  # remove punctuation marks
        words = re.split(r'\W+', text)
        return len(words)
        
    
    
    def filter_entries(self):
        if self.word_count== 'more':
            filtered_entries = [entry for entry in self.entries if entry['words']> self.reference_number ]
        else:
            filtered_entries = [entry for entry in self.entries if entry['words']<= self.reference_number ]
        return filtered_entries


    def order_entries(self,filtered_entries):
        return sorted(filtered_entries, key=lambda x: x[self.order_by], reverse=self.order)
        
       
    def run(self):
        self.get_data_entries()  
        filtered_entries = self.filter_entries()   
        print(self.order_entries(filtered_entries))
        
        
if __name__ == '__main__':
    scraper = Scraper('https://news.ycombinator.com/',30,5,'less','comments', True)
    scraper.run()