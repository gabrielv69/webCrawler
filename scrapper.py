from database_manager import DatabaseManager
from bs4 import BeautifulSoup
from datetime import datetime
import requests
import re

"""Definition for scrapper class
author: Gabriel Vivas
create: 04/09/2024"""

class Scrapper:
    request_timestamp = None
    filtered_length= 0
    def __init__(self,url,max_entries,reference_number,word_count,order_by,order):
        self.base_url = url
        self.max_entries=max_entries
        self.reference_number=reference_number
        self.word_count=word_count
        self.order_by=order_by
        self.order=order
        self.entries = []
        self.db = DatabaseManager('database/usage_data.db')
        

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
        self.filtered_length= len(filtered_entries)
        return filtered_entries


    def order_entries(self,filtered_entries):
        return sorted(filtered_entries, key=lambda x: x[self.order_by], reverse=self.order)
    
    def store_usage_data(self):
        create_table_query = '''
            CREATE TABLE IF NOT EXISTS usage_data (
                timestamp TEXT,
                reference_value TEXT,
                word_count TEXT,
                order_by TEXT,
                order_type TEXT,
                result_length TEXT
            )
        '''
        self.db.execute_query(create_table_query)
        insert_query =("INSERT INTO usage_data (timestamp,reference_value, word_count,order_by,order_type,result_length) VALUES (?,?,?,?,?,?)")
        data_to_insert = (
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),  
            self.reference_number, 
            self.word_count,  
            self.order_by,  
            'DESC' if self.order else 'ASC',  
            self.filtered_length 
        )
        self.db.execute_query(insert_query, data_to_insert)
       
    def close_connection(self):
        self.db.close()
    
    def show_scraping_data(self):
        rows = self.db.fetch_all("SELECT * FROM usage_data")
        print('='*24 + ' USAGE DATA ' +'='*24)
        for row in rows:
            print(row)
              
    def run(self):
        self.get_data_entries()  
        filtered_entries = self.filter_entries() 
        self.order_entries(filtered_entries)  
        self.store_usage_data()
        self.show_scraping_data()
        self.close_connection()
        
        